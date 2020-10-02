#!/usr/bin/env python3
from typing import Any, List
import typing
import logging
import inspect
import uuid


logger = logging.getLogger(__name__)


class Instance:
    '''Instance tool'''
    def __init__(self, region: str, uuid: uuid.UUID, verbosity: int = 1, dry: bool = False, quiet: bool = True):
        self.region = region
        self.uuid = str(uuid)
        self.verbosity = verbosity
        self.dry = dry
        self.quiet = quiet

    def __repr__(self):
        rep = f"{self.uuid} - {self.region}"
        if self.dry:
            rep += " (dry)"
        return rep

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self=} : rebooting {force=}")

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self=} : rebooting hard")
        self.reboot(force=True)


class Instances:
    '''Instance tool'''
    def __init__(self, region: str, uuids: List[uuid.UUID], flags: List[str] = [], verbosity: int = 1, dry: bool = False, quiet: bool = True):
        self.region = region
        self.flags = flags
        self.instances = [Instance(region=region, uuid=uuid, verbosity=verbosity, dry=dry, quiet=quiet) for uuid in uuids]
        self.dry = dry

    def __repr__(self):
        rep = f"{len(self.instances)} instances - {self.region} - {self.flags=}"
        if self.dry:
            rep += " (dry)"
        return rep

    def reboot(self, force: bool = False):
        '''Reboot an instance'''
        print(f"{self=} : rebooting {force=}")
        for instance in self.instances:
            instance.reboot(force)

    def reboot_hard(self):
        '''Reboot hard instance'''
        print(f"{self=} : rebooting hard")
        for instance in self.instances:
            instance.reboot_hard()


classes_to_gen = [Instance, Instances]
prog_name = 'unity'
version = '0.0.1'

code = f'''
import click
from click_skeleton import AdvancedGroup, skeleton

@skeleton(name='{prog_name}', version='{version}')
def cli():
    pass

'''

for class_to_gen in classes_to_gen:
    constructor_signature = inspect.signature(class_to_gen.__init__)
    constructor_parameters = constructor_signature.parameters.copy()
    del constructor_parameters['self']
    constructor_arguments = ', '.join(constructor_parameters.keys())
    code += f'''
@click.group('{class_to_gen.__name__.lower()}', help='{class_to_gen.__doc__}', cls=AdvancedGroup)
def {class_to_gen.__name__.lower()}_cli():
    pass
'''
    method_list = {
        func.replace("_", "-"): func
        for func in dir(class_to_gen)
        if callable(getattr(class_to_gen, func)) and not func.startswith("_")
    }
    for command_name, method_name in method_list.items():
        method = getattr(class_to_gen, method_name)
        method_docstring = method.__doc__
        method_signature = inspect.signature(method)
        method_parameters = method_signature.parameters.copy()
        del method_parameters['self']
        method_arguments = ', '.join(method_parameters.keys())
        command_arguments = ', '.join(constructor_parameters.keys())
        if method_parameters:
            command_arguments += ', ' + method_arguments

        code += f'''

@{class_to_gen.__name__.lower()}_cli.command('{command_name}', short_help='{method_docstring}')'''

        for constructor_parameter in constructor_parameters.values():

            if constructor_parameter.default is inspect.Parameter.empty:
                code += f"""
@click.argument(
    '{constructor_parameter.name}"""
            else:
                code += f"""
@click.option(
    '--{constructor_parameter.name}"""

            if constructor_parameter.annotation is bool:
                code += f"""/--no-{constructor_parameter.name}',
    is_flag=True,
    default={constructor_parameter.default},
    show_default=True,"""
            else:
                code += f"""',"""

            if typing.get_origin(constructor_parameter.annotation) is list:
                if constructor_parameter.default is inspect.Parameter.empty:
                    code += f'''
    nargs=-1,'''
                else:
                    code += f'''
    multiple=True,'''

            if constructor_parameter.annotation is uuid.UUID:
                code += f'''
    type=click.UUID,'''
            elif constructor_parameter.annotation is str:
                code += f'''
    type=click.STRING,'''
            elif constructor_parameter.annotation is float:
                code += f'''
    type=click.FLOAT,'''
            elif constructor_parameter.annotation is int:
                code += f'''
    type=click.INT,'''
            code += f'''
)'''

        for method_parameter in method_parameters.values():
            print(f'{method_parameter=} : {method_parameter.annotation}')
            if method_parameter.default is inspect.Parameter.empty:
                code += f'''
@click.argument('{method_parameter.name}')'''
            elif method_parameter.annotation is bool:
                code += f'''
@click.option(
    '--{method_parameter.name}/--no-{method_parameter.name}',
    type={method_parameter.annotation.__name__},
    default={method_parameter.default},
    show_default=True,
)'''

        code += f'''
def {method_name}({command_arguments}):
    {class_to_gen.__name__.lower()} = {class_to_gen.__name__}({constructor_arguments})
    {class_to_gen.__name__.lower()}.{method_name}({method_arguments})
'''
    code += f'''
cli.add_group({class_to_gen.__name__.lower()}_cli, '{class_to_gen.__name__.lower()}')
'''

code += f'''
cli.main(prog_name='{prog_name}')
'''


def main():
    print(code)
    exec(code)  # pylint: disable=exec-used


if __name__ == '__main__':
    main()

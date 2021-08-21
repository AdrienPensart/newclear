from typing import Union, List
from pprint import pformat
import logging
import uuid
import inspect
import typing
import inflection
from ordered_set import OrderedSet  # type: ignore

logger = logging.getLogger(__name__)


class CliGenerator:
    def __init__(self, prog_name, version, classes):
        self.prog_name = prog_name
        self.version = version
        self.classes = {
            class_ref.__name__: GroupGenerator(class_ref, self)
            for class_ref in classes
        }

    def generate(self):
        code = '''#!/usr/bin/env python3
import sys
import click
from click_skeleton import AdvancedGroup, skeleton
'''

        for class_ref in self.classes.values():
            code += f'''
from newclear.{class_ref.snake} import {class_ref.name}'''

        code += f'''


@skeleton(name='{self.prog_name}', version='{self.version}')
def cli():
    pass

'''
        for class_ref in self.classes.values():
            code += class_ref.generate()
            logger.error("\n")

        code += f'''
sys.exit(cli.main(prog_name='{self.prog_name}'))'''
        return code


class GroupGenerator:
    def __init__(self, class_ref, cli_generator):
        self.cli_generator = cli_generator
        self.class_ref = class_ref
        self.options_help = {}
        self.cmd_aliases = {}
        self.aliases = []
        self.constructor_signature = inspect.signature(self.constructor)
        for key, value in inspect.getmembers(self.class_ref):
            if key.startswith('_'):
                continue
            if key == 'aliases' and isinstance(value, list):
                self.aliases = value
                continue
            elems = key.split('_')
            if len(elems) < 2:
                continue

            name = '_'.join(elems[0:-1])
            if elems[-1] == "help":
                self.options_help[name] = value
            elif elems[-1] == "aliases" and isinstance(value, list):
                self.cmd_aliases[name] = value

        self.methods = []
        for method_name in dir(self.class_ref):
            if callable(getattr(self.class_ref, method_name)) and not method_name.startswith("_"):
                command_name = method_name.replace("_", "-")
                method = CommandGenerator(command_name, method_name, self.cmd_aliases.get(method_name, []), self)
                self.methods.append(method)

    def __repr__(self):
        return f"{self.name}"

    def get_method(self, name):
        return getattr(self.class_ref, name)

    @property
    def constructor(self):
        return self.class_ref.__init__

    @property
    def constructor_parameters(self):
        parameters = self.constructor_signature.parameters.copy()
        del parameters['self']
        return parameters

    @property
    def constructor_arguments(self):
        return list(self.constructor_parameters.keys())

    @property
    def name(self):
        return self.class_ref.__name__

    @property
    def instance(self):
        joined_constructor_arguments = ', '.join(self.constructor_arguments)
        return f'''{self.snake} = {self.name}({joined_constructor_arguments})'''

    @property
    def doc(self):
        return self.class_ref.__doc__

    @property
    def snake(self):
        return inflection.underscore(self.name)

    def generate(self):
        code = f'''
@click.group('{self.snake}', help='{self.doc}', cls=AdvancedGroup, aliases={pformat(self.aliases)})
def {self.snake}_cli():
    pass
'''
        for method in self.methods:
            logger.error(f"\nGenerating {method}")
            code += method.generate()

        code += f'''

cli.add_group({self.snake}_cli, '{self.snake}')

'''
        return code

    def generate_constructor_parameters(self, method_generator=None):
        code = ""
        for parameter in self.constructor_parameters.values():
            code += self.generate_parameter(parameter, method_generator)
        return code

    def generate_parameter(self, parameter, method_generator=None):
        default_value = parameter.default
        annotation = parameter.annotation
        logger.error(f"{self} : {parameter=} | {default_value=} | {annotation=} | {method_generator=}")
        origin = typing.get_origin(annotation)
        args = typing.get_args(annotation)
        help_string = self.options_help.get(parameter.name, "")
        code = ""

        if (origin is None or origin is list) and default_value is inspect.Parameter.empty:
            if origin is not None and origin is list:
                annotation = args[0]
                logger.error(f"{parameter} : new annotation {annotation}")
            code += f'''
@click.argument(
    '{parameter.name}'''
        else:
            code += f'''
@click.option(
    '--{parameter.name}'''

        if annotation is bool:
            code += f"""/--no-{parameter.name}',
    is_flag=True,"""
        else:
            code += """',"""

        if origin is list and default_value is inspect.Parameter.empty:
            code += '''
    nargs=-1,'''
        elif origin is Union:
            new_args = typing.get_args(args[0])
            new_origin = typing.get_origin(args[0])
            if new_origin is list:
                annotation = new_args[0]
                logger.error(f"{parameter=} : new {annotation=}")
                help_string += '  [multiple]'
                code += '''
    multiple=True,'''

        elif default_value is not inspect.Parameter.empty:
            code += f'''
    default={default_value},
    show_default=True,'''

        if annotation is bool:
            pass
        elif annotation is uuid.UUID:
            code += '''
    type=click.UUID,'''
        elif annotation is str:
            code += '''
    type=click.STRING,'''
        elif annotation is float:
            code += '''
    type=click.FLOAT,'''
        elif annotation is int:
            code += '''
    type=click.INT,'''
        else:
            class_name = annotation.__name__
            if class_name in self.cli_generator.classes:
                if method_generator:
                    logger.error(f"Adding intermediate class {class_name} to {method_generator}")
                    method_generator.intermediate_classes.add(self.cli_generator.classes[class_name])
                return self.cli_generator.classes[class_name].generate_constructor_parameters(method_generator)

        if help_string:
            code += f'''
    help="{help_string}",'''
        code += '''
)'''
        return code


class CommandGenerator:
    def __init__(self, command_name: str, method_name: str, command_aliases: List[str], class_ref: GroupGenerator):
        self.command_name = command_name
        self.method_name = method_name
        self.command_aliases = command_aliases
        self.class_ref = class_ref
        self.method = self.class_ref.get_method(self.method_name)
        self.method_docstring = self.method.__doc__
        self.method_signature = inspect.signature(self.method)
        self.method_parameters = self.method_signature.parameters.copy()
        self.intermediate_classes = OrderedSet()
        del self.method_parameters['self']
        self.method_arguments = list(self.method_parameters.keys())

    def __repr__(self):
        return f"{self.command_name=} | {self.method_name=}"

    def generate(self):
        code = f'''

@{self.class_ref.snake}_cli.command('{self.command_name}', short_help='{self.method_docstring}', aliases={pformat(self.command_aliases)})'''

        code += self.class_ref.generate_constructor_parameters(self)

        for method_parameter in self.method_parameters.values():
            logger.error(f"generating {method_parameter} with {self}")
            code += self.class_ref.generate_parameter(method_parameter, self)

        intermediate_arguments = OrderedSet()
        for intermediate_class in self.intermediate_classes:
            for constructor_argument in intermediate_class.constructor_arguments:
                intermediate_arguments.add(constructor_argument)

        command_arguments = OrderedSet(self.class_ref.constructor_arguments + list(intermediate_arguments) + self.method_arguments)
        joined_command_arguments = ', '.join(command_arguments)
        joined_method_arguments = ', '.join(self.method_arguments)

        intermediate_instances = ""
        for intermediate_class in self.intermediate_classes:
            intermediate_instances += f"    {intermediate_class.instance}\n"

        code += f'''
def {self.class_ref.snake}_{self.method_name}({joined_command_arguments}):
{intermediate_instances}
    {self.class_ref.instance}
    {self.class_ref.snake}.{self.method_name}({joined_method_arguments})
'''

        return code

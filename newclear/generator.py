import uuid
import inspect
import typing

def codegen(prog_name, version, classes_to_gen):
    code = f'''#!/usr/bin/env python3
import click
import sys
from click_skeleton import AdvancedGroup, skeleton
'''
    for class_to_gen in classes_to_gen:
        code += f'''
from newclear.{class_to_gen.__name__.lower()} import {class_to_gen.__name__}'''
    code += f'''

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
sys.exit(cli.main(prog_name='{prog_name}'))
'''
    return code

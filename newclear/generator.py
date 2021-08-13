from typing import Union
import logging
import uuid
import inspect
import typing

logger = logging.getLogger(__name__)


def codegen(prog_name, version, classes_to_gen):
    code = '''#!/usr/bin/env python3
import sys
import click
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
        options_help = {}
        for key, value in inspect.getmembers(class_to_gen):
            if key.startswith('_'):
                continue
            elems = key.split('_')
            if len(elems) < 2:
                continue
            if elems[-1] != "help":
                continue
            options_help['_'.join(elems[0:-1])] = value

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
            class_name = class_to_gen.__name__.lower()
            if method_parameters:
                command_arguments += ', ' + method_arguments

            code += f'''

@{class_name}_cli.command('{command_name}', short_help='{method_docstring}')'''

            for constructor_parameter in constructor_parameters.values():
                default_value = constructor_parameter.default
                annotation = constructor_parameter.annotation
                origin = typing.get_origin(annotation)
                args = typing.get_args(annotation)
                help_string = options_help.get(constructor_parameter.name, "")
                # logger.error(f"{constructor_parameter} : origin = {origin} | args = {args} | default value = {default_value}")

                if (origin is None or origin is list) and default_value is inspect.Parameter.empty:
                    if origin is not None and origin is list:
                        annotation = args[0]
                        # logger.error(f"{constructor_parameter} : new annotation {annotation}")
                    code += f'''
@click.argument(
    '{constructor_parameter.name}'''
                else:
                    code += f'''
@click.option(
    '--{constructor_parameter.name}'''

                if annotation is bool:
                    code += f"""/--no-{constructor_parameter.name}',
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
                        # logger.error(f"{constructor_parameter} : new annotation {annotation}")
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
                    logger.error(f"Unsupported param : {annotation}, defaults to string")

                if help_string:
                    code += f'''
    help="{help_string}",'''
                code += '''
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
def {class_name}_{method_name}({command_arguments}):
    {class_to_gen.__name__.lower()} = {class_to_gen.__name__}({constructor_arguments})
    {class_to_gen.__name__.lower()}.{method_name}({method_arguments})
'''
        code += f'''

cli.add_group({class_to_gen.__name__.lower()}_cli, '{class_to_gen.__name__.lower()}')

'''

    code += f'''
sys.exit(cli.main(prog_name='{prog_name}'))'''
    return code

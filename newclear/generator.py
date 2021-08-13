from typing import Union
import logging
import uuid
import inspect
import typing
import inflection

logger = logging.getLogger(__name__)


def codegen(prog_name, version, classes):
    code = '''#!/usr/bin/env python3
import sys
import click
from click_skeleton import AdvancedGroup, skeleton
'''
    classes_to_gen = [ClassToGen(class_ref) for class_ref in classes]
    for class_to_gen in classes_to_gen:
        code += f'''
from newclear.{class_to_gen.snake} import {class_to_gen.name}'''
    code += f'''


@skeleton(name='{prog_name}', version='{version}')
def cli():
    pass

'''
    for class_to_gen in classes_to_gen:
        code += class_to_gen.gen()

    code += f'''
sys.exit(cli.main(prog_name='{prog_name}'))'''
    return code


class ClassToGen:
    def __init__(self, class_ref):
        self.class_ref = class_ref
        self.options_help = {}
        self.constructor_signature = inspect.signature(self.constructor)
        for key, value in inspect.getmembers(self.class_ref):
            if key.startswith('_'):
                continue
            elems = key.split('_')
            if len(elems) < 2:
                continue
            if elems[-1] != "help":
                continue
            self.options_help['_'.join(elems[0:-1])] = value

        self.method_list = {}
        for func in dir(self.class_ref):
            if callable(getattr(self.class_ref, func)) and not func.startswith("_"):
                self.method_list[func.replace("_", "-")] = func

    @property
    def constructor(self):
        return self.class_ref.__init__

    @property
    def name(self):
        return self.class_ref.__name__

    @property
    def doc(self):
        return self.class_ref.__doc__

    @property
    def snake(self):
        return inflection.underscore(self.name)

    def gen(self):
        code = f'''
@click.group('{self.snake}', help='{self.doc}', cls=AdvancedGroup)
def {self.snake}_cli():
    pass
'''
        for command_name, method_name in self.method_list.items():
            code += self.gen_method(command_name, method_name)

        code += f'''

cli.add_group({self.snake}_cli, '{self.snake}')

'''
        return code

    def gen_constructor_parameters(self, constructor_parameters):
        code = ""
        for constructor_parameter in constructor_parameters.values():
            code += self.gen_parameter(constructor_parameter)
        return code

    def gen_parameter(self, parameter):
        default_value = parameter.default
        annotation = parameter.annotation
        origin = typing.get_origin(annotation)
        args = typing.get_args(annotation)
        help_string = self.options_help.get(parameter.name, "")
        logger.error(f"{parameter} : origin = {origin} | args = {args} | default value = {default_value}")
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
                logger.error(f"{parameter} : new annotation {annotation}")
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
        return code

    def gen_method(self, command_name, method_name):
        constructor_parameters = self.constructor_signature.parameters.copy()
        del constructor_parameters['self']
        constructor_arguments = ', '.join(constructor_parameters.keys())

        method = getattr(self.class_ref, method_name)
        method_docstring = method.__doc__
        method_signature = inspect.signature(method)
        method_parameters = method_signature.parameters.copy()
        del method_parameters['self']
        method_arguments = ', '.join(method_parameters.keys())
        command_arguments = ', '.join(constructor_parameters.keys())
        if method_parameters:
            command_arguments += ', ' + method_arguments

        code = f'''

@{self.snake}_cli.command('{command_name}', short_help='{method_docstring}')'''

        code += self.gen_constructor_parameters(constructor_parameters)

        for method_parameter in method_parameters.values():
            code += self.gen_parameter(method_parameter)

        code += f'''
def {self.snake}_{method_name}({command_arguments}):
    {self.snake} = {self.name}({constructor_arguments})
    {self.snake}.{method_name}({method_arguments})
'''

        return code

import logging
import inspect
from newclear.group_generator import GroupGenerator

logger = logging.getLogger(__name__)


class CliGenerator:
    def __init__(self, prog_name, version, module):
        self.module = module
        self.prog_name = prog_name
        self.version = version
        self.classes = {}
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                self.classes[obj.__name__] = GroupGenerator(obj, self)

    def generate(self):
        code = '''#!/usr/bin/env python3
import sys
import click
from click_skeleton import AdvancedGroup, skeleton
'''

        for class_ref in self.classes.values():
            code += f'''
from {self.module.__name__}.{class_ref.snake} import {class_ref.name}'''

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

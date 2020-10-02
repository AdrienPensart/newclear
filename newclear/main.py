#!/usr/bin/env python3
from typing import Any, List
import typing
import inspect
import uuid

from newclear.instance import Instance
from newclear.instances import Instances
from newclear.generator import codegen

classes_to_gen = [Instance, Instances]
prog_name = 'unity'
version = '0.0.1'


def main():
    code = codegen(prog_name, version, classes_to_gen)
    print(code)
    exec(code)  # pylint: disable=exec-used


if __name__ == '__main__':
    main()

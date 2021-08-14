#!/usr/bin/env python3
from newclear.region import Region
from newclear.instance import Instance
from newclear.aggregate import Aggregate
from newclear.instances import Instances
from newclear.generator import CliGenerator

classes_to_gen = [Region, Aggregate, Instance, Instances]
prog_name = 'unity'
version = '0.0.1'


def main():
    cli_generator = CliGenerator(prog_name, version, classes_to_gen)
    code = cli_generator.generate()
    print(code)


if __name__ == '__main__':
    main()

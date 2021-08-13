#!/usr/bin/env python3
from newclear.region import Region
from newclear.region_instance import RegionInstance
# from newclear.instance import Instance
# from newclear.instances import Instances
from newclear.generator import codegen

# classes_to_gen = [Region, Instance, Instances]
classes_to_gen = [Region, RegionInstance]
prog_name = 'unity'
version = '0.0.1'


def main():
    code = codegen(prog_name, version, classes_to_gen)
    print(code)


if __name__ == '__main__':
    main()

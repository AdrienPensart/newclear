#!/usr/bin/env python3
import sys
import importlib
import stat
import os
import click
from click_skeleton import skeleton
from newclear.cli_generator import CliGenerator

prog_name = 'newclear'
version = '0.0.1'


@skeleton(name=prog_name, version=version, auto_envvar_prefix='NC')
def cli():
    '''Class to CLI generator'''


@cli.command()
@click.argument('package', type=click.Path(file_okay=False, exists=True))
@click.argument('output', type=click.File('w'))
@click.option('--prog-name', help="Program name", default='unity')
@click.option('--version', help="Version string", default='1.0.0')
def generate(output, package, prog_name, version):
    '''Generate a CLI'''
    module = importlib.import_module(package)
    cli_generator = CliGenerator(prog_name=prog_name, version=version, module=module)
    code = cli_generator.generate()
    output.write(code)
    st = os.stat(output.name)
    os.chmod(output.name, st.st_mode | stat.S_IEXEC)


def main(**kwargs):
    exit_code = cli.main(prog_name=prog_name, **kwargs)
    return exit_code


if __name__ == '__main__':
    sys.exit(main())

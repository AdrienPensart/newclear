#!/usr/bin/env python3
import click
import sys
from click_skeleton import AdvancedGroup, skeleton

from newclear.instance import Instance
from newclear.instances import Instances

@skeleton(name='unity', version='0.0.1')
def cli():
    pass


@click.group('instance', help='Instance tool', cls=AdvancedGroup)
def instance_cli():
    pass


@instance_cli.command('reboot', short_help='Reboot an instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.argument(
    'uuid',
    type=click.UUID,
)
@click.option(
    '--verbosity',
    type=click.INT,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    '--quiet/--no-quiet',
    is_flag=True,
    default=True,
    show_default=True,
)
@click.option(
    '--force/--no-force',
    type=bool,
    default=False,
    show_default=True,
)
def reboot(region, uuid, verbosity, dry, quiet, force):
    instance = Instance(region, uuid, verbosity, dry, quiet)
    instance.reboot(force)


@instance_cli.command('reboot-hard', short_help='Reboot hard instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.argument(
    'uuid',
    type=click.UUID,
)
@click.option(
    '--verbosity',
    type=click.INT,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    '--quiet/--no-quiet',
    is_flag=True,
    default=True,
    show_default=True,
)
def reboot_hard(region, uuid, verbosity, dry, quiet):
    instance = Instance(region, uuid, verbosity, dry, quiet)
    instance.reboot_hard()

cli.add_group(instance_cli, 'instance')

@click.group('instances', help='Instance tool', cls=AdvancedGroup)
def instances_cli():
    pass


@instances_cli.command('reboot', short_help='Reboot an instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.argument(
    'uuids',
    nargs=-1,
)
@click.option(
    '--flags',
    multiple=True,
)
@click.option(
    '--verbosity',
    type=click.INT,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    '--quiet/--no-quiet',
    is_flag=True,
    default=True,
    show_default=True,
)
@click.option(
    '--force/--no-force',
    type=bool,
    default=False,
    show_default=True,
)
def reboot(region, uuids, flags, verbosity, dry, quiet, force):
    instances = Instances(region, uuids, flags, verbosity, dry, quiet)
    instances.reboot(force)


@instances_cli.command('reboot-hard', short_help='Reboot hard instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.argument(
    'uuids',
    nargs=-1,
)
@click.option(
    '--flags',
    multiple=True,
)
@click.option(
    '--verbosity',
    type=click.INT,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    '--quiet/--no-quiet',
    is_flag=True,
    default=True,
    show_default=True,
)
def reboot_hard(region, uuids, flags, verbosity, dry, quiet):
    instances = Instances(region, uuids, flags, verbosity, dry, quiet)
    instances.reboot_hard()

cli.add_group(instances_cli, 'instances')

sys.exit(cli.main(prog_name='unity'))


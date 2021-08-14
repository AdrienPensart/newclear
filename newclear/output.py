#!/usr/bin/env python3
import sys
import click
from click_skeleton import AdvancedGroup, skeleton

from newclear.region import Region
from newclear.aggregate import Aggregate
from newclear.instance import Instance
from newclear.instances import Instances


@skeleton(name='unity', version='0.0.1')
def cli():
    pass


@click.group('region', help='Region tool', cls=AdvancedGroup)
def region_cli():
    pass


@region_cli.command('show', short_help='None')
@click.argument(
    'region',
    type=click.STRING,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
def region_show(region, dry):

    region = Region(region, dry)
    region.show()


cli.add_group(region_cli, 'region')


@click.group('aggregate', help='Aggregate tool', cls=AdvancedGroup)
def aggregate_cli():
    pass


@aggregate_cli.command('show', short_help='None')
@click.argument(
    'region',
    type=click.STRING,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument(
    'aggregate',
    type=click.STRING,
)
def aggregate_show(region, aggregate, dry):
    region = Region(region, dry)

    aggregate = Aggregate(region, aggregate)
    aggregate.show()


cli.add_group(aggregate_cli, 'aggregate')


@click.group('instance', help='Instance tool', cls=AdvancedGroup)
def instance_cli():
    pass


@instance_cli.command('reboot', short_help='Reboot an instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument(
    'uuid',
    type=click.UUID,
)
@click.option(
    '--force/--no-force',
    is_flag=True,
    default=False,
    show_default=True,
    help="Force action",
)
def instance_reboot(region, uuid, dry, force):
    region = Region(region, dry)

    instance = Instance(region, uuid)
    instance.reboot(force)


@instance_cli.command('reboot-hard', short_help='Reboot hard instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument(
    'uuid',
    type=click.UUID,
)
def instance_reboot_hard(region, uuid, dry):
    region = Region(region, dry)

    instance = Instance(region, uuid)
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
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument(
    'uuids',
    nargs=-1,
    type=click.UUID,
)
@click.option(
    '--force/--no-force',
    is_flag=True,
    default=False,
    show_default=True,
    help="Force action",
)
def instances_reboot(region, uuids, dry, force):
    region = Region(region, dry)

    instances = Instances(region, uuids)
    instances.reboot(force)


@instances_cli.command('reboot-hard', short_help='Reboot hard instance')
@click.argument(
    'region',
    type=click.STRING,
)
@click.option(
    '--dry/--no-dry',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument(
    'uuids',
    nargs=-1,
    type=click.UUID,
)
def instances_reboot_hard(region, uuids, dry):
    region = Region(region, dry)

    instances = Instances(region, uuids)
    instances.reboot_hard()


cli.add_group(instances_cli, 'instances')


sys.exit(cli.main(prog_name='unity'))

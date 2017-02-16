#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Release a new version of the defined software sets
#######################################################################################################################

import click
import os
import re

@click.command(short_help='Bump the general release of the RESIF deployment.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
@click.option('--major', flag_value=True, help='Update major version.')
@click.option('--minor', flag_value=True, help='Update minor version.')
@click.option('--patch', flag_value=True, help='Update patch version.')
def bump(configdir, major, minor, patch):
    configdir = os.path.abspath(os.path.expandvars(configdir))
    if not os.path.isdir(configdir):
        click.echo("Invalid configdir %s." % configdir, err=True)
        raise click.Abort
    if sum([major, minor, patch]) != 1:
        click.echo("Please specify exactly one of {major|minor|patch}.", err=True)
        raise click.Abort

    version_file = open(os.path.join(configdir, "VERSION"), 'r')
    version = version_file.readline()
    version_file.close()

    click.echo("Previous version was %s." % version)

    match = re.match("^([0-9]+)\.([0-9]+)\.([0-9]+)$", version)

    new_version = version

    if patch:
        new_version = "%s.%s.%s" % (match.group(1), match.group(2), int(match.group(3)) + 1)
    elif minor:
        new_version = "%s.%s.%s" % (match.group(1), int(match.group(2)) + 1, 0)
    elif major:
        new_version = "%s.%s.%s" % (int(match.group(1)) + 1, 0, 0)

    click.echo("New version is %s." % new_version)

    version_file = open(os.path.join(configdir, "VERSION"), 'w')
    version_file.write(new_version)
    version_file.close()

    return
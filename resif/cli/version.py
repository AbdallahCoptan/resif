#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Prints Resif's version information.
#######################################################################################################################

import click
import os

@click.command(short_help="Prints Resif's version information.")
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
def version(configdir):
    configdir = os.path.abspath(os.path.expandvars(configdir))
    if not os.path.isdir(configdir):
        click.echo("Invalid configdir %s." % configdir, err=True)
        raise click.Abort

    version_file = open(os.path.join(configdir, "VERSION"), 'r')
    version = version_file.readline()
    version_file.close()

    click.echo("%s" % version)

    return
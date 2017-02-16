#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: List all available software sets.
#######################################################################################################################

import click
import os
from resif.utilities import swset

@click.command(short_help='List all available software sets.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
def list(configdir):
    configdir = os.path.abspath(os.path.expandvars(configdir))
    if not os.path.isdir(configdir):
        click.echo("Invalid configdir %s." % configdir, err=True)
        raise click.Abort
    swset.listSoftwareSets(configdir)
    return
#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Create a new recipe / software sets definition.
#######################################################################################################################

import click
import os
from resif.utilities import swset

@click.command(short_help='Create a new recipe / software sets definition.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
@click.argument('name')
def new(**kwargs):

    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    if not os.path.isdir(kwargs['configdir']):
        click.echo("Invalid configdir %s." % kwargs['configdir'], err=True)
        raise click.Abort

    if os.path.isfile(os.path.join(kwargs['configdir'], "swsets", "%s.yaml" % kwargs['name'])):
        click.echo("A software set with the name '%s' already exists." % kwargs['name'], err=True)
        raise click.Abort

    swset.add(kwargs['name'], kwargs['configdir'])
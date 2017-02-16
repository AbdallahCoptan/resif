#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Display detailed information about a software set.
#######################################################################################################################

import click
import os
from resif.utilities import swset

@click.command(short_help='Display detailed information about a software set.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
@click.argument('swset')
def info(**kwargs):

    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    if not os.path.isdir(kwargs['configdir']):
        click.echo("Invalid configdir %s." % kwargs['configdir'], err=True)
        raise click.Abort

    # If a yaml file was given for the swset argument
    if kwargs['swset'].endswith(".yaml"):
        if os.path.isfile(kwargs['swset']):
            click.echo("Loading software sets from file %s.\n" % (kwargs['swset']))
            kwargs['swset'] = os.path.abspath(os.path.expandvars(kwargs['swset']))
        else:
            click.echo("File %s cannot be found." % (kwargs['swset']), err=True)
            raise click.Abort
    # If we just got a name for the swset
    else:
        # Look for the respective yaml file in the configuration directory
        swsetfile = kwargs['swset'] + ".yaml"
        if os.path.isfile(os.path.join(kwargs['configdir'], "swsets", swsetfile)):
            click.echo("Loading software set '%s' from configdir %s.\n" %(kwargs['swset'], kwargs['configdir']))
            kwargs['swset'] = os.path.join(kwargs['configdir'], "swsets", swsetfile)
        else:
            click.echo("Software set %s cannot be found in configdir %s." % (kwargs['swset'], kwargs['configdir']), err=True)
            raise click.Abort

    swset.info(kwargs['swset'])
    return
import os
import shutil
import subprocess
import sys

import click

from resif.utilities import source
from resif.utilities import role
from resif.utilities import swset


@click.command(short_help='Deploy software sets on an existing installatation.')
# Configuration
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
# Software building variables
@click.option('--installdir', 'installdir', envvar='RESIF_INSTALLDIR', help="Use if you don't want to deploy the software inside the <datadir>. Softwares will then be deployed in <installdir>/<swset>/modules")
@click.option('--buildmode', envvar='RESIF_BUILDMODE', type=click.Choice(['local', 'job']), default='local', help='Mode to build the software: either building locally or in a job.')
@click.option('--role', envvar='RESIF_ROLE', default='default', help='Role configuration to use.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-options', 'eb_options', envvar='RESIF_EB_OPTIONS', help='Any command line options to pass to EasyBuild for the build.')
@click.argument('swset')
def build(**kwargs):
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    if kwargs['installdir']:
        kwargs['installdir'] = os.path.abspath(os.path.expandvars(kwargs['installdir']))

    if kwargs['swset'].endswith(".yaml"):
        if os.path.isfile(kwargs['swset']):
            click.echo("Loading software sets from file %s" % (kwargs['swset']))
            kwargs['swset'] = os.path.abspath(os.path.expandvars(kwargs['swset']))
        else:
            sys.stderr.write("File %s cannot be found.\n" % (kwargs['swset']))
            exit(50)
    else:
        swsetfile = kwargs['swset'] + ".yaml"
        if os.path.isfile(os.path.join(kwargs['configdir'], "swsets", swsetfile)):
            click.echo("Loading software set '%s' from configdir %s" %(kwargs['swset'], kwargs['configdir']))
            kwargs['swset'] = os.path.join(kwargs['configdir'], "swsets", swsetfile)
        else:
            sys.stderr.write("Software set %s cannot be found in configdir %s.\n" % (kwargs['swset'], kwargs['configdir']))
            exit(50)

    print kwargs
    return
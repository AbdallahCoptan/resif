#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Release a new version of the defined software sets
#######################################################################################################################

import click

from resif.cli.build import build

@click.command(short_help='Release a new version of the defined software sets.')
# Configuration
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
# Software building variables
@click.option('--role', envvar='RESIF_ROLE', help='Role configuration to use.')
@click.option('--eb-prefix', 'eb_prefix', envvar='EASYBUILD_PREFIX', default='$HOME/.local/easybuild', help='Prefix directory for Easybuild installation.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-options', 'eb_options', envvar='RESIF_EB_OPTIONS', help='Any command line options to pass to EasyBuild for the build.')
@click.option('--enable-try', 'enable_try', flag_value=True, help='Set this flag if you want to try building with similar toolchains if no easyconfig file is found.')
@click.argument('swset')
def release(**kwargs):

    kwargs['release'] = True
    build(**kwargs)

    return

#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Release a new version of the defined software sets
#######################################################################################################################

import click
import os
from resif.utilities import source

@click.group(short_help='Show or modify available sources.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to put the configuration in.')
@click.pass_context
def sources(ctx, configdir):
    configdir = os.path.abspath(os.path.expandvars(configdir))
    if not os.path.isdir(configdir):
        click.echo("Invalid configdir %s." % configdir, err=True)
        exit(50)
    else:
        ctx.obj = {'configdir': configdir}
    return

@sources.command()
@click.argument('sourcename')
@click.pass_context
def add(ctx, sourcename):
    return

@sources.command()
@click.pass_context
def list(ctx):
    source.list(ctx.obj['configdir'])

@sources.command()
@click.confirmation_option(prompt='Are you sure you want to delete the source definition?')
@click.argument('sourcename')
@click.pass_context
def rm(ctx, sourcename):
    source.remove(sourcename, ctx.obj['configdir'])

@sources.command()
@click.argument('sourcename')
@click.pass_context
def info(ctx, sourcename):
    source.info(sourcename, ctx.obj['configdir'])
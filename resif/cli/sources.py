#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Release a new version of the defined software sets
#######################################################################################################################

import click
import os
import re
from resif.utilities import source

@click.group(short_help='Show or modify available sources.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from..')
@click.pass_context
def sources(ctx, configdir):
    configdir = os.path.abspath(os.path.expandvars(configdir))
    if not os.path.isdir(configdir):
        click.echo("Invalid configdir %s." % configdir, err=True)
        exit(50)
    else:
        ctx.obj = {'configdir': configdir}
    return

@sources.command(short_help='Add a new source.')
@click.argument('sourcename')
@click.pass_context
def add(ctx, sourcename):
    if re.match("^\w+$", sourcename):
        source.add(sourcename, ctx.obj['configdir'])
    else:
        click.echo("The sourcename should only contain letters, numbers and '_'.", err=True)
        raise click.Abort

@sources.command(short_help='List all sources.')
@click.pass_context
def list(ctx):
    source.list(ctx.obj['configdir'])

@sources.command(short_help='Remove a source.')
@click.confirmation_option(prompt='Are you sure you want to delete the source definition?')
@click.argument('sourcename')
@click.pass_context
def rm(ctx, sourcename):
    source.remove(sourcename, ctx.obj['configdir'])

@sources.command(short_help='Print details about a source.')
@click.argument('sourcename')
@click.pass_context
def info(ctx, sourcename):
    source.info(sourcename, ctx.obj['configdir'])
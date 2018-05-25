#######################################################################################################################
# Author: Sarah Diehl, Maxime Schmitt
# Mail: hpc-sysadmins@uni.lu
# Overview: Module that combines all the other modules and provides a CLI.
#######################################################################################################################

import click
import pkg_resources
import os
import fcntl
import errno

from .cli.init import init
from .cli.build import build
from .cli.release import release
from .cli.sources import sources
from .cli.bump import bump
from .cli.version import version
from .cli.list import list
from .cli.info import info
from .cli.new import new
from .cli.modules import modules

lock_file = os.path.join(os.path.expanduser("~"), 'resif.lock')
fp = open(lock_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except (IOError, OSError) as e:
    if e.errno != errno.EAGAIN and e.errno != errno.EACCES:
        click.echo("Could not obtain lock on %s." % lock_file, err=True)
        raise
    else:
        # another instance is running
        exit("Another instance of RESIF is already runing. Exiting.")

#######################################################################################################################
# The resif group. Defines the name of the command. It is the "main" group.
@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', flag_value=True, help='Return the version of this script.')
def resif(ctx, version):
    """
    RESIF commandline interface.

    Choose the sub-command you want to execute.
    """

    if ctx.invoked_subcommand is None:
        if version:
            click.echo("This is RESIF version " + pkg_resources.require("resif")[0].version)
        else:
            click.echo(ctx.get_help())

#######################################################################################################################

# Add the different CLI commands
resif.add_command(init)
resif.add_command(build)
resif.add_command(release)
resif.add_command(sources)
resif.add_command(bump)
resif.add_command(version)
resif.add_command(list)
resif.add_command(info)
resif.add_command(new)
resif.add_command(modules)

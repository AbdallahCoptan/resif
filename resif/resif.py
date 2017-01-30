#######################################################################################################################
# Author: Sarah Diehl, Maxime Schmitt
# Mail: hpc-sysadmins@uni.lu
# Overview: Module that combines all the other modules and provides a CLI.
#######################################################################################################################

import click
import subprocess
import pkg_resources

from .cli.init import init
from .cli.build import build
from .cli.release import release


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
            subprocess.check_call(['resif', '--help'])

#######################################################################################################################

# Add the different CLI commands
resif.add_command(init)
resif.add_command(build)
resif.add_command(release)
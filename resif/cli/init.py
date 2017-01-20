#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Initialize the directories for configuration and installation and installs EasyBuild
#######################################################################################################################

import os
import shutil
import subprocess
import sys
import urllib
import tempfile
import pkg_resources

import click

from git import Repo

from resif.utilities import source

# Initialize the configuration directory
def initializeConfig(params):
    click.echo("Creating RESIF configuration.")

    # If a git reposistory was specified for the configuration, simply pull it
    if params["git_resif_control"]:
        # clone git repo with configuration
        Repo.clone_from(params['git_resif_control'], params['configdir'])

    # otherwise initialize from templates
    else:
        template = pkg_resources.resource_filename("resif", '/'.join(('templates', 'configdir')))

        subprocess.check_output("rsync --exclude '*.mako' -avzu %s/ %s/" % (template, params['configdir']), shell=True)

        # Set the version to 0.0.1
        version_file = open(os.path.join(params["configdir"], "VERSION"), 'w')
        version_file.write("0.0.1")
        version_file.close()

    click.echo("Configuration created successfully.")

# Initialize the data directory (where software will be installed)
def initializeDatadir(params):
    click.echo("Initializing DATADIR.")

    # Create directories for devel and production branches
    os.makedirs(params["datadir"])
    os.mkdir(os.path.join(params["datadir"], "devel"))
    os.mkdir(os.path.join(params["datadir"], "production"))

    # Create directories for easyconfigs and easyblocks
    os.mkdir(os.path.join(params["datadir"], "easyblocks"))
    os.mkdir(os.path.join(params["datadir"], "easyconfigs"))

    # Create symlinks for easy access to specific versions
    os.symlink("devel", os.path.join(params["datadir"], "testing"))
    os.symlink(os.path.join("production", "last"), os.path.join(params["datadir"], "stable"))

    # Pull default easyconfig and easyblocks repository
    source.pullall(params["configdir"], params["datadir"])
    click.echo("DATADIR initialized successfully.")

# Install EasyBuild
def bootstrapEB(prefix, mns, module_tool):
    click.echo("Bootstrapping EasyBuild. This might take a few minutes.")

    # Create a temporary directory to save the bootstrap script from EasyBuild
    tmpdir = tempfile.mkdtemp()
    installscript = os.path.join(tmpdir, "bootstrap_eb.py")

    # Download the bootstrap script from the EasyBuild github repository
    installscripturl = urllib.URLopener()
    installscripturl.retrieve("https://raw.githubusercontent.com/hpcugent/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py", installscript)

    # Prepare log files
    log = open(os.path.join(tmpdir, "bootstrap_eb.log"), 'w')
    errlog = open(os.path.join(tmpdir, "bootstrap_eb.err.log"), 'w')

    # Try to run the bootstrap script
    try:
        subprocess.check_call("EASYBUILD_MODULES_TOOL=%s EASYBUILD_MODULE_NAMING_SCHEME=%s python %s %s" % (module_tool, mns, installscript, prefix), shell=True, stdout=log, stderr=errlog)
    # Upon failure, keep the temporary directory with the log files and point the user to it
    except subprocess.CalledProcessError:
        sys.stderr.write("EasyBuild installation failed. Logfiles can be found in %s\n" % (tmpdir))
        log.close()
        errlog.close()
        exit(50)

    log.close()
    errlog.close()

    # Upon successful installation of EasyBuild, remove the temporary directory with the bootstrap script and log files
    shutil.rmtree(tmpdir, True)

    click.echo("Bootstrapping ended successfully. EasyBuild MODULEPATH is %s" % (os.path.join(prefix, "modules", "all")))
    return

# Initialize the necessary directories and install EasyBuild
@click.command(short_help='This command sets up a working RESIF environment and installs EasyBuild.')
@click.option('--git-resif-control', 'git_resif_control', envvar='RESIF_GIT_RESIF_CONTROL', help='Defines a git repository URL to get the configuration from.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to put the configuration in.')
@click.option('--datadir', 'datadir', envvar='RESIF_DATADIR', default='$HOME/.local/resif', help='Path to the root directory for apps (contains all the architecture correspondig to RESIF).')
@click.option('--eb-prefix', 'eb_prefix', envvar='EASYBUILD_PREFIX', default='$HOME/.local/easybuild', help='Prefix directory for Easybuild installation.')
@click.option('--eb-module-tool', 'eb_module_tool', envvar='EASYBUILD_MODULES_TOOL', type=click.Choice(['Lmod', 'EnvironmentModulesTcl', 'EnvironmentModulesC']), default='Lmod', help='Name of module tool.')
@click.option('--mns', 'mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'HierarchicalMNS', 'CategorizedModuleNamingScheme', 'CategorizedHMNS']), default='CategorizedModuleNamingScheme', help='Module Naming Scheme to be used.')
@click.option('--overwrite', 'overwrite', flag_value=True, envvar='RESIF_OVERWRITE', help='Set this flag if you want to overwrite any existing directories in the CONFIGDIR and DATADIR.')
def init(**kwargs):

    # Make sure all paths are absolute and with variables expanded
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    kwargs['datadir'] = os.path.abspath(os.path.expandvars(kwargs['datadir']))
    kwargs['eb_prefix'] = os.path.abspath(os.path.expandvars(kwargs['eb_prefix']))

    # If the configuration directory already exists
    if os.path.isdir(kwargs["configdir"]):
        # If overwrite was specified, delete the full configuration directory
        if kwargs["overwrite"]:
            shutil.rmtree(kwargs["configdir"], True)
        # Otherwise exit, tell the user why and point to the overwrite option
        else:
            sys.stderr.write("An installation is already present at your configdir: " + kwargs["configdir"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + kwargs["configdir"] + " and " + kwargs["datadir"] + "\033[0m\n")
            exit(50)

    # If the data directory already exists
    if os.path.isdir(kwargs["datadir"]):
        # If overwrite was specified, delete the full data directory
        if kwargs["overwrite"]:
            shutil.rmtree(kwargs["datadir"], True)
        # Otherwise exit, tell the user why and point to the overwrite option
        else:
            sys.stderr.write("An installation is already present at your datadir: " + kwargs["datadir"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + kwargs["configdir"] + " and " + kwargs["datadir"] + "\033[0m\n")
            exit(50)

    # Initialize configuration directory
    initializeConfig(kwargs)
    # Initialize data directory and pull default easyconfigs and easyblocks repositories
    initializeDatadir(kwargs)
    # Install EasyBuild in <eb_prefix> directory
    bootstrapEB(kwargs["eb_prefix"], kwargs["mns"], kwargs["eb_module_tool"])

    click.echo("Finished initialization of RESIF. Please add the following lines to your .bashrc (or similar):\n\nexport RESIF_CONFIGDIR=%s\nexport EASYBUILD_PREFIX=%s\nexport EASYBUILD_MODULES_TOOL=%s\n" % (kwargs['configdir'], kwargs['eb_prefix'], kwargs['eb_module_tool']))


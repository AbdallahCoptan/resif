import os
import shutil
import subprocess
import sys
import urllib
import tempfile

import click

from resif.utilities import source
from resif.utilities import role
from resif.utilities import swset

def initializeConfig(params):
    click.echo("Creating RESIF configuration.")
    if params["git_resif_control"]:
        # clone git repo with configuration
        subprocess.check_call(['git', 'clone', params['git_resif_control'], params['configdir']])
    else:
        # manually create configdir layout
        rolespath = os.path.join(params['configdir'], 'roles')
        sourcespath = os.path.join(params['configdir'], 'sources')
        swsetspath = os.path.join(params['configdir'], 'swsets')
        os.makedirs(params["configdir"])
        os.mkdir(rolespath)
        os.mkdir(sourcespath)
        os.mkdir(swsetspath)

        source.createDefaultSource(params)
        role.createDefaultRole(params)
        swset.createDefaultSwset(params)

        version_file = open(os.path.join(params["configdir"], "VERSION"), 'w')
        version_file.write("0.0.1")
        version_file.close()
    click.echo("Configuration created successfully.")

def initializeDatadir(params):
    click.echo("Initializing DATADIR.")
    os.makedirs(params["datadir"])
    os.mkdir(os.path.join(params["datadir"], "devel"))
    os.mkdir(os.path.join(params["datadir"], "production"))
    os.mkdir(os.path.join(params["datadir"], "easyblocks"))
    os.mkdir(os.path.join(params["datadir"], "easyconfigs"))
    os.symlink("devel", os.path.join(params["datadir"], "testing"))
    os.symlink(os.path.join("production", "last"), os.path.join(params["datadir"], "stable"))
    click.echo("DATADIR initialized successfully.")

def bootstrapEB(prefix, mns, module_tool):
    click.echo("Bootstrapping EasyBuild. This might take a few minutes.")
    tmpdir = tempfile.mkdtemp()
    installscript = os.path.join(tmpdir, "bootstrap_eb.py")
    installscripturl = urllib.URLopener()
    installscripturl.retrieve("https://raw.githubusercontent.com/hpcugent/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py", installscript)

    log = open(os.path.join(tmpdir, "bootstrap_eb.log"), 'w')
    errlog = open(os.path.join(tmpdir, "bootstrap_eb.err.log"), 'w')

    try:
        subprocess.check_call("EASYBUILD_MODULES_TOOL=%s EASYBUILD_MODULE_NAMING_SCHEME=%s python %s %s" % (module_tool, mns, installscript, prefix), shell=True, stdout=log, stderr=errlog)
    except subprocess.CalledProcessError:
        sys.stderr.write("EasyBuild installation failed. Logfiles can be found in %s\n" % (tmpdir))
        exit(50)

    log.close()
    errlog.close()

    shutil.rmtree(tmpdir, True)
    click.echo("Bootstrapping ended successfully.")
    return

# Initialize the necessary directories
@click.command(short_help='This command sets up a working RESIF environment and installs EasyBuild.')
@click.option('--git-resif-control', 'git_resif_control', envvar='RESIF_GIT_RESIF_CONTROL', help='Defines a git repository URL to get the configuration from.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to put the configuration in.')
@click.option('--datadir', 'datadir', envvar='RESIF_DATADIR', default='$HOME/.local/resif', help='Path to the root directory for apps (contains all the architecture correspondig to RESIF).')
@click.option('--eb-prefix', 'eb_prefix', envvar='EASYBUILD_PREFIX', default='$HOME/.local/easybuild', help='Prefix directory for Easybuild installation.')
@click.option('--eb-module-tool', 'eb_module_tool', envvar='EASYBUILD_MODULES_TOOL', type=click.Choice(['Lmod', 'EnvironmentModulesTcl', 'EnvironmentModulesC']), default='Lmod', help='Name of module tool.')
@click.option('--mns', 'mns', envvar='EASYBUILD_MODULE_NAMING_SCHEME', type=click.Choice(['EasyBuildMNS', 'HierarchicalMNS', 'CategorizedModuleNamingScheme', 'CategorizedHMNS']), default='CategorizedModuleNamingScheme', help='Module Naming Scheme to be used.')
@click.option('--overwrite', 'overwrite', flag_value=True, envvar='RESIF_OVERWRITE', help='Set this flag if you want to overwrite any existing directories in the CONFIGDIR and DATADIR.')
def init(**kwargs):
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    kwargs['datadir'] = os.path.abspath(os.path.expandvars(kwargs['datadir']))
    kwargs['eb_prefix'] = os.path.abspath(os.path.expandvars(kwargs['eb_prefix']))

    if os.path.isdir(kwargs["configdir"]):
        if kwargs["overwrite"]:
            shutil.rmtree(kwargs["configdir"], True)
        else:
            sys.stderr.write("An installation is already present at your configdir: " + kwargs["configdir"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + kwargs["configdir"] + " and " + kwargs["datadir"] + "\033[0m\n")
            exit(50)

    if os.path.isdir(kwargs["datadir"]):
        if kwargs["overwrite"]:
            shutil.rmtree(kwargs["datadir"], True)
        else:
            sys.stderr.write("An installation is already present at your datadir: " + kwargs["datadir"] + "\nPlease use the --overwrite flag if you want to overwrite this installation.\n" + "\033[93m" + "WARNING: This will remove everything at " + kwargs["configdir"] + " and " + kwargs["datadir"] + "\033[0m\n")
            exit(50)


    initializeConfig(kwargs)
    initializeDatadir(kwargs)
    bootstrapEB(kwargs["eb_prefix"], kwargs["mns"], kwargs["eb_module_tool"])


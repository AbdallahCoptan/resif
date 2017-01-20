

import os
import subprocess
import time
import re

import click

from resif.utilities import source
from resif.utilities import role
from resif.utilities.swset import getSoftwareLists

# Check if a command exists in the current environment
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

# Build a list of software with EasyBuild
def buildSwSets(params):

    # Get lists of software that should be installed from the swset configuration file
    swlists = getSoftwareLists(params['swset'])

    # Check which module tool is present on the system
    if cmd_exists("lmod"):
        params['module_cmd'] = "lmod"
    elif cmd_exists("modulecmd"):
        params["module_cmd"] = "modulecmd"
    else:
        click.echo("Neither modulecmd nor lmod has been found in your path. Please install either one of them to continue. (Preferably choose lmod for more functionalities)", err=True)
        exit(40)

    # For each software set (or list of softwares)
    for swset in swlists.keys():

        if 'role' in params and params['role']:
            roledata = role.get(params['role'],params['configdir'])
        elif os.path.isfile(os.path.join(params['configdir'], "%s.yaml" % (swset))):
            roledata = role.get(swset, params['configdir'])
        else:
            roledata = role.get("default", params['configdir'])

        # Pull all easyconfig and easyblocks repositories and the paths to them
        eblockspath, econfigspath = source.pullall(params['configdir'], roledata['datadir'], params['swset'])

        # Set the command line options for the eb command
        options = ""

        if 'eb_buildpath' in params and params['eb_buildpath']:
            options += ' --buildpath=' + params['eb_buildpath']
        if 'eb_options' in params and params['eb_options']:
            options += " " + params["eb_options"]
        if econfigspath:
            options += ' --robot=' + econfigspath
        else:
            options += ' --robot'
        options += ' --module-naming-scheme=' + roledata['mns']

        click.echo("Building '%s'..." % (swset))
        
        if not ('installdir' in params and params['installdir']):
            params['installdir'] = os.path.join(roledata['datadir'], "devel")
        
        installpath =  os.path.join(params['installdir'], swset)

        # We add the place where the software will be installed to the MODULEPATH for the duration of the installation
        # so that EasyBuild will not instantly forget that it has installed them after it is done (problematic for dependency resolution)
        # We also add the EB_PREFIX to ensure that EasyBuild will be available

        ebInstallPath = os.path.join(params['eb_prefix'], 'modules', 'all')
        defaultSwsetPath = os.path.join(params['installdir'], "default")

        oldmodulepath = ""
        if 'MODULEPATH' in os.environ and os.environ['MODULEPATH']:
            oldmodulepath = os.environ['MODULEPATH']

        # Part for environment-modules
        if params["module_cmd"] == "modulecmd":
            if oldmodulepath:
                os.environ['MODULEPATH'] = ':'.join([oldmodulepath, os.path.join(params['installdir'], 'modules', 'all'), ebInstallPath, defaultSwsetPath])
            else:
                os.environ['MODULEPATH'] = ':'.join([os.path.join(params['installdir'], 'modules', 'all'), ebInstallPath, defaultSwsetPath])

        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # Part for Lmod
        if params["module_cmd"] == "lmod":
            process.stdin.write("module use " + ebInstallPath + "\n")
            process.stdin.write("module use " + defaultSwsetPath + "\n")
            process.stdin.write("module use " + os.path.join(params['installdir'], 'modules', 'all') + "\n")

        # Load EasyBuild module
        if roledata['mns'] == "CategorizedModuleNamingScheme":
            process.stdin.write('module load tools/EasyBuild\n')
        else:
            process.stdin.write('module load EasyBuild\n')

        # remove EB_PREFIX since it's not in our data directory and might contain further modules than just EasyBuild,
        # that could interfer with our installation
        if params["module_cmd"] == "modulecmd":
            os.environ['MODULEPATH'] = ':'.join([oldmodulepath, os.path.join(params['installdir'], 'modules', 'all'), defaultSwsetPath])
        elif params["module_cmd"] == "lmod":
            # only remove it if it wasn't present before
            if ebInstallPath not in oldmodulepath.split(":"):
                process.stdin.write("module unuse " + ebInstallPath + "\n")

        # Add path to easyblocks to PYTHONPATH, so EasyBuild can find them
        if eblockspath:
            process.stdin.write('export PYTHONPATH=$PYTHONPATH:' + eblockspath + '\n')

        alreadyInstalled = False

        swsetStart = time.time()

        # For each software
        for software in swlists[swset]:
            click.echo("Now starting to install " + software[:-3])

            # Call EasyBuild with all options to install software
            process.stdin.write('eb ' + options + ' --installpath=' + installpath + ' ' + software + '\n')
            # Print exit code at the end to know if installation was successful
            process.stdin.write('echo $?\n')

            out = ""
            # Check output of installation line by line
            while True:
                out = process.stdout.readline()
                # Check if the module was already present, then no installation happened
                if re.search("\(module found\)", out) != None:
                    alreadyInstalled = True

                # Try if we arrived at the line with the exit code
                try:
                    i = int(out)
                except ValueError:
                    i = -1
                # If we haven't arrived at the exit code, just print out the line
                if i < 0:
                    click.echo(out, nl=False)
                # If we are at the exit code, inform the user about the success or failure of the installation
                # and break the loop of reading the output
                # Since our main process is still running, we have to know when we reached the last line with content,
                # otherwise readline() will wait forever for another line of output that never comes
                else:
                    if i == 0:
                        if alreadyInstalled:
                            click.echo(software[:-3] + " was already installed. Nothing to be done.\n")
                            alreadyInstalled = False
                        else:
                            click.echo('Successfully installed ' + software[:-3])
                    else:
                        click.echo('Failed to install ' + software[:-3] + '\n' + 'Operation failed with return code ' + out, err=True)
                        exit(out)
                    break

        process.terminate()

        # Compute how long the installation took
        swsetEnd = time.time()
        swsetDuration = swsetEnd - swsetStart
        m, s = divmod(swsetDuration, 60)
        h, m = divmod(m, 60)
        swsetDurationStr = "%dh %dm %ds" % (h, m, s)

        click.echo("Software set '" + swset + "' successfully installed. Build duration: " + swsetDurationStr)

    return


@click.command(short_help='Deploy software sets on an existing installatation.')
# Configuration
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path to load the configuration from.')
# Software building variables
@click.option('--installdir', 'installdir', envvar='RESIF_INSTALLDIR', help="Use if you don't want to deploy the software inside the <datadir>. Softwares will then be deployed in <installdir>/<swset>/modules")
@click.option('--role', envvar='RESIF_ROLE', help='Role configuration to use.')
@click.option('--eb-prefix', 'eb_prefix', envvar='EASYBUILD_PREFIX', default='$HOME/.local/easybuild', help='Prefix directory for Easybuild installation.')
@click.option('--eb-buildpath', 'eb_buildpath', envvar='EASYBUILD_BUILDPATH', help='EasyBuild buildpath.')
@click.option('--eb-options', 'eb_options', envvar='RESIF_EB_OPTIONS', help='Any command line options to pass to EasyBuild for the build.')
@click.argument('swset')
def build(**kwargs):

    # Make sure all paths are absolute and with variables expanded
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    kwargs['eb_prefix'] = os.path.abspath(os.path.expandvars(kwargs['eb_prefix']))

    if kwargs['eb_buildpath']:
        kwargs['eb_buildpath'] = os.path.abspath(os.path.expandvars(kwargs['eb_buildpath']))

    if kwargs['installdir']:
        kwargs['installdir'] = os.path.abspath(os.path.expandvars(kwargs['installdir']))

    # If a yaml file was given for the swset argument
    if kwargs['swset'].endswith(".yaml"):
        if os.path.isfile(kwargs['swset']):
            click.echo("Loading software sets from file %s" % (kwargs['swset']))
            kwargs['swset'] = os.path.abspath(os.path.expandvars(kwargs['swset']))
        else:
            click.echo("File %s cannot be found." % (kwargs['swset']), err=True)
            exit(50)
    # If we just got a name for the swset
    else:
        # Look for the respective yaml file in the configuration directory
        swsetfile = kwargs['swset'] + ".yaml"
        if os.path.isfile(os.path.join(kwargs['configdir'], "swsets", swsetfile)):
            click.echo("Loading software set '%s' from configdir %s" %(kwargs['swset'], kwargs['configdir']))
            kwargs['swset'] = os.path.join(kwargs['configdir'], "swsets", swsetfile)
        else:
            click.echo("Software set %s cannot be found in configdir %s." % (kwargs['swset'], kwargs['configdir']), err=True)
            exit(50)

    click.echo("Building the software sets...")
    start = time.time()

    buildSwSets(kwargs)

    # Compute how long the installation took
    end = time.time()
    duration = end - start
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    durationFormated = "%dh %dm %ds" % (h, m, s)
    click.echo("All software sets successfully installed. Build duration: " + durationFormated)

    return

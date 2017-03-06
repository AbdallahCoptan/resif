#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Build list of software defined in a resifile
#######################################################################################################################

import os
import grp
import subprocess
import time
import re
import datetime
import glob

import click

from resif.utilities import source
from resif.utilities import role
from resif.utilities.swset import getSoftwareSets, getSoftwares

def chgrp(path, groupname):
    click.echo("\nChanging permissions of installation directory. This might take a few minutes.")
    try:
        gid = grp.getgrnam(groupname).gr_gid
        os.chown(path, -1, gid)
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chown(os.path.join(root, d), -1, gid)
            for f in files:
                os.chown(os.path.join(root, f), -1, gid)
    except KeyError:
        click.echo("\033[93mFailed to change permissions of installation directory. Unknown group '%s', please check that this group exists on the system!\033[0m\n" % groupname, err=True)

# Determine correct install directory
def getInstallDir(configdir, datadir, release=False):
    if release:
        filename = os.path.join(configdir, "VERSION")
        v = open(filename, 'r')
        version = v.readline()
        v.close()
        match = re.match("^([0-9]+)\.([0-9]+)\.([0-9]+)$", version)
        if match:
            shortversion = "%s.%s" % (match.group(1), match.group(2))
            search = glob.glob(os.path.join(datadir, "production", "v%s-*" % (shortversion)))
            if search:
                return search[0]
            else:
                installdir = os.path.join(datadir, "production", "v%s-%s" % (shortversion, datetime.datetime.now().strftime("%Y%m%d")))
                os.mkdir(installdir)
                os.symlink(installdir, os.path.join(datadir, "production", "v%s" % (shortversion)))
                last = os.path.join(datadir, "production", "last")
                if os.path.islink(last):
                    os.remove(last)
                os.symlink(installdir, last)
                return installdir
        else:
            click.echo("Invalid version string found in %s." % (filename), err=True)
            exit(50)
    else:
        return os.path.join(datadir, "devel")

# Check if a command exists in the current environment
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def execRToutput(cmd):
    output = []
    cmd = "export PYTHONUNBUFFERED=1; %s" % cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable="/bin/bash")
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() is not None:
            break
        if line:
            output.append(line)
            click.echo(line.strip())
    rc = process.poll()
    return ''.join(output), rc

# Returns True if we have good eb files for all softwares
# otherwise returns False
def checkSoftwares(softwares, enable_try):
    for software, swinfohash in softwares.items():
        if (not swinfohash['ebfile']) or ('try' in swinfohash and not enable_try):
            click.echo("Could not find easyconfig file for '%s'" % software, err=True)
            return False
    return True

# Build a list of software with EasyBuild
def buildSwSets(params):

    # Keep track of software build success & failure
    statistics = {'success': [],
                  'already_installed': [],
                  'no_ebfile': [],
                  'failed': []}

    # Get lists of software that should be installed from the swset configuration file
    swsets = getSoftwareSets(params['swset'])

    # Check which module tool is present on the system
    if cmd_exists("lmod"):
        params['module_cmd'] = "lmod"
    elif cmd_exists("modulecmd"):
        params["module_cmd"] = "modulecmd"
    else:
        click.echo("Neither modulecmd nor lmod has been found in your path. Please install either one of them to continue. (Preferably choose lmod for more functionalities)", err=True)
        exit(40)

    # For each software set
    for swset in swsets:

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

        if params['dry_run']:
            click.echo("Dry run of software set '%s'..." % (swset))
        else:
            click.echo("Building software set '%s'..." % (swset))

        if 'release' in params and params['release']:
            params['installdir'] = getInstallDir(params['configdir'], roledata['datadir'], params['release'])
        else:
            if not ('installdir' in params and params['installdir']):
                params['installdir'] = getInstallDir(params['configdir'], roledata['datadir'])
        
        installpath =  os.path.join(params['installdir'], swset)

        # We add the place where the software will be installed to the MODULEPATH for the duration of the installation
        # so that EasyBuild will not instantly forget that it has installed them after it is done (problematic for dependency resolution)
        # We also add the EB_PREFIX to ensure that EasyBuild will be available

        precommands = ""

        # If additional environmental variables are defined in the role, export them
        if 'environment' in roledata and isinstance(roledata['environment'], dict):
            for variablename, value in roledata['environment'].items():
                precommands += 'export %s=%s;' % (variablename, value)

        ebInstallPath = os.path.join(params['eb_prefix'], 'modules', 'all')
        defaultSwsetPath = os.path.join(params['installdir'], "default")

        oldmodulepath = ""
        if 'MODULEPATH' in os.environ and os.environ['MODULEPATH']:
            oldmodulepath = os.environ['MODULEPATH']

        # Part for environment-modules
        if params["module_cmd"] == "modulecmd":
            precommands += 'export MODULEPATH=$MODULEPATH:%s;' % (ebInstallPath)
        # Part for Lmod
        elif params["module_cmd"] == "lmod":
            precommands += "module use %s;" % (ebInstallPath)

        # Load EasyBuild module
        if roledata['mns'] == "CategorizedModuleNamingScheme":
            precommands += 'module load tools/EasyBuild;'
        else:
            precommands += 'module load EasyBuild;'

        # remove EB_PREFIX since it's not in our data directory and might contain further modules than just EasyBuild,
        # that could interfer with our installation
        if params["module_cmd"] == "modulecmd":
            precommands += 'export MODULEPATH=%s;' % (':'.join([oldmodulepath, os.path.join(params['installdir'], 'modules', 'all'), defaultSwsetPath]))
        elif params["module_cmd"] == "lmod":
            # only remove it if it wasn't present before
            if ebInstallPath not in oldmodulepath.split(":"):
                precommands += "module unuse %s; " % (ebInstallPath)
            precommands += "module use %s; module use %s;" % (defaultSwsetPath, os.path.join(params['installdir'], 'modules', 'all'))

        # Add path to easyblocks to PYTHONPATH, so EasyBuild can find them
        if eblockspath:
            precommands += 'export PYTHONPATH=$PYTHONPATH:%s;' % (eblockspath)

        swsetStart = time.time()

        softwares = getSoftwares(params['swset'],swset,econfigspath)

        if not params['ignore_build_failure']:
            if not checkSoftwares(softwares, params['enable_try']):
                raise click.Abort

        # For each software
        for software, swinfohash in softwares.items():
            if params['dry_run']:
                click.echo("Now starting dry run of " + software)
            else:
                click.echo("Now starting to install " + software)

            if swinfohash['ebfile'] and (('try' not in swinfohash) or params['enable_try']):
                if 'try' in swinfohash and swinfohash['try']:
                    command = "%s eb %s --installpath=%s --try-toolchain=%s %s\n" % (precommands, options, installpath, swinfohash['try'], swinfohash['ebfile'])
                else:
                    command = "%s eb %s --installpath=%s %s\n" % (precommands, options, installpath, swinfohash['ebfile'])

                # Call EasyBuild with all options to install software
                output, returncode = execRToutput(command)
                if not returncode:
                    if re.search("\(module found\)", output) != None:
                        click.echo(software + " was already installed. Nothing to be done.")
                        statistics['already_installed'].append(software)
                    elif not params['dry_run']:
                        click.echo('Successfully installed ' + software)
                        statistics['success'].append(software)
                else:
                    match = re.search("Results of the build can be found in the log file\(s\) (.*)", output)
                    if match:
                        logfile = match.group(1)
                        statistics['failed'].append("%s (log: %s)" % (software, logfile))
                    else:
                        statistics['failed'].append(software)
                    click.echo('Failed to install %s.\nOperation failed with return code %s.' % (software, returncode), err=True)
                    if not params['ignore_build_failure']:
                        exit(returncode)
            else:
                click.echo("Failed to install %s.\nNo easyconfig file found." % (software), err=True)
                if not params['ignore_build_failure']:
                    exit(-1)
                statistics['no_ebfile'].append(software)

        # Compute how long the installation took
        swsetEnd = time.time()
        swsetDuration = swsetEnd - swsetStart
        m, s = divmod(swsetDuration, 60)
        h, m = divmod(m, 60)
        swsetDurationStr = "%dh %dm %ds" % (h, m, s)

        if 'group' in roledata and roledata['group']:
            chgrp(installpath, roledata['group'])

        if not params['dry_run']:
            click.echo("Finished build of software set '" + swset + "'. Duration: " + swsetDurationStr)

    click.echo("\n=== SUMMARY STATISTICS ===")
    click.echo("Successfully installed: %s" % (len(statistics['success'])))
    click.echo("Already installed:      %s" % (len(statistics['already_installed'])))

    if params['ignore_build_failure']:
        click.echo("No .eb file found:      %s" % (len(statistics['no_ebfile'])))
        click.echo("Build failed:           %s" % (len(statistics['failed'])))

        if statistics['no_ebfile']:
            click.echo("\nList of softwares without .eb file:")
            for software in statistics['no_ebfile']:
                click.echo("- %s" % (software))

        if statistics['failed']:
            click.echo("\nList of failed softwares:")
            for software in statistics['failed']:
                click.echo("- %s" % (software))

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
@click.option('--enable-try', 'enable_try', flag_value=True, help='Set this flag if you want to try building with similar toolchains if no easyconfig file is found.')
@click.option('--ignore-build-failure', 'ignore_build_failure', flag_value=True, help='Continue even if the build of a software fails.')
@click.argument('swset')
def build(**kwargs):

    # Make sure all paths are absolute and with variables expanded
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))
    if not os.path.isdir(kwargs['configdir']):
        click.echo("Invalid configdir %s." % kwargs['configdir'], err=True)
        exit(50)

    kwargs['eb_prefix'] = os.path.abspath(os.path.expandvars(kwargs['eb_prefix']))
    if not os.path.isdir(kwargs['eb_prefix']):
        click.echo("Invalid EasyBuild prefix %s." % kwargs['eb_prefix'], err=True)
        exit(50)

    if kwargs['eb_buildpath']:
        kwargs['eb_buildpath'] = os.path.abspath(os.path.expandvars(kwargs['eb_buildpath']))
        if not os.path.isdir(kwargs['eb_buildpath']):
            click.echo("Invalid EasyBuild buildpath %s." % kwargs['eb_buildpath'], err=True)
            exit(50)

    if kwargs['installdir']:
        kwargs['installdir'] = os.path.abspath(os.path.expandvars(kwargs['installdir']))
        if not os.path.isdir(kwargs['installdir']):
            click.echo("Invalid installdir %s." % kwargs['installdir'], err=True)
            exit(50)

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

    if kwargs['eb_options'] and re.search("(^|\s)--dry-run(\s|$)|(^|\s)--dry-run-short(\s|$)|(^|\s)-D(\s|$)", kwargs['eb_options']):
        kwargs['dry_run'] = True
    else:
        kwargs['dry_run'] = False

    if kwargs['dry_run']:
        click.echo("Doing a dry run...")
    else:
        click.echo("Building the software sets...")
    start = time.time()

    buildSwSets(kwargs)

    # Compute how long the installation took
    end = time.time()
    duration = end - start
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    durationFormated = "%dh %dm %ds" % (h, m, s)
    if kwargs['dry_run']:
        click.echo("\nFinished dry run in %s." % (durationFormated))
    else:
        click.echo("\nFinished build of all software sets. Duration: " + durationFormated)

    return

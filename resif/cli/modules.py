#######################################################################################################################
# Author: Valentin Plugaru
# Mail: hpc-sysadmins@uni.lu
# Overview: Create hierarchy of environment modules to allow switching between different build releases
#######################################################################################################################

import os
import errno
import glob
import shutil
import time
import datetime
import jinja2

from distutils.version import LooseVersion

import click

from resif.utilities import role

@click.command(short_help='Create modules hierarchy to allow switching software releases.')
@click.option('--configdir', 'configdir', envvar='RESIF_CONFIGDIR', default='$HOME/.config/resif', help='Defines an alternative path for the configuration.')
@click.option('--role', envvar='RESIF_ROLE', default='default', help='Role configuration to use (default: "default").')
@click.option('--datadir', 'datadir', envvar='RESIF_INSTALLDIR', help="Explicitly set root of builds to determine modules hierarchy from, otherwise taken from configdir/role configuration or $RESIF_INSTALLDIR.")
@click.option('--moduledir', 'moduledir', envvar='RESIF_MODULEDIR', help='Explicitly set root for modules hierarchy, otherwise taken from configdir/modules configuration or $RESIF_MODULEDIR.')
@click.option('--overwrite', 'overwrite', flag_value=True, help='Enable Resif to overwrite existing dirs/files in MODULEDIR.')
@click.option('--no-op', 'noop', flag_value=True, help='Just print operations to be performed.')
@click.option('--prod-in-root', 'prodinroot', flag_value=True, help="Add production swsets' modules directly to root.")

def modules(**kwargs):

    if kwargs['noop']: click.echo("==== Running in NO-OP, will just print operations.")

    ## Set up command line / environment parameters and checks
    # Make sure all paths are absolute and with variables expanded
    kwargs['configdir'] = os.path.abspath(os.path.expandvars(kwargs['configdir']))

    # Determine data directory which we'll traverse to find build releases
    if not os.path.isdir(kwargs['configdir']):
        click.echo("Invalid configdir: %s." % kwargs['configdir'], err=True)
        exit(50)
    if 'datadir' in kwargs and kwargs['datadir']:
        datadir = kwargs['datadir']
    else:
	roledata = getRoleData(kwargs)
        if 'datadir' in roledata and roledata['datadir']:
            datadir = roledata['datadir']
	else:
            click.echo("Cannot determine datadir from configdir/role.", err=True)
            exit(50)
    if 'moduledir' in kwargs and kwargs['moduledir']:
        moduledir = kwargs['moduledir']
    else:
        roledata = getRoleData(kwargs)
        if 'moduledir' in roledata and roledata['moduledir']:
            datadir = roledata['moduledir']
	else:
            click.echo("Cannot determine moduledir from configdir/role.", err=True)
            exit(50)

    if not os.path.isdir(datadir):
        click.echo("Invalid datadir %s." % kwargs['datadir'], err=True)
        exit(50)
    datadir = os.path.abspath(os.path.expandvars(datadir))
    click.echo("==== Using data dir: %s" % datadir)

    # Confirm module directory
    if os.path.isdir(moduledir):
        if kwargs['overwrite']:
            click.echo("==== Found existing modules dir: %s and --overwrite is set, cleaning it and continuing." % moduledir, err=True)
            if not kwargs['noop']: shutil.rmtree(moduledir, ignore_errors=True) 
        else:
            click.echo("==== Found existing modules dir: %s but --overwrite is not set, so stopping." % moduledir, err=True)
            exit(50)
    else:
        click.echo("==== Will create modules dir: %s" % moduledir)

    # Warn if asked not to create
    if kwargs['prodinroot']: click.echo("==== Will not create `production` directory level, swsets go in root.")

    ## MAIN execution code
    # Find directories that correspond to software environment builds
    buildsdata = findBuilds(datadir)
    # Create SWEnv objects (with self-categorizing code) from builds paths
    swenvs = []
    for path in buildsdata['production']: swenvs.append(SWEnv(path, 'production', moduledir, addtypelevel = not kwargs['prodinroot']))
    for path in buildsdata['devel']: swenvs.append(SWEnv(path, 'devel', moduledir, addtypelevel=False))
    # Allow some environments to multiple modules, some with priority in the hierarchy
    SWEnv.prioritizeModules(swenvs)
    # Generate modules for each environment
    for swenv in swenvs: swenv.generateModules(noop=kwargs['noop'])
    
    return

def getRoleData(**kwargs):
    ''' Read and return role-based configuration data '''
    rolefile = os.path.join(kwargs['configdir'], 'roles', "%s.yaml" % (kwargs['role']))
    if not os.path.isfile(rolefile):
        click.echo("Cannot read role file %s." % rolefile, err=True)
        exit(50)
    roledata = role.get(kwargs['role'], kwargs['configdir'])
    return roledata

def findBuilds(rootdir):
    ''' Find build directories based on current naming scheme '''
    # Catch: production/v0.1-20170602/default production/v0.1-20170602/bioinfo
    prodBuildDirs = glob.glob(os.path.join(rootdir, "production", "v*-[0-9]*", "*"))
    # Catch: devel/default devel/bioinfo
    develBuildDirs = glob.glob(os.path.join(rootdir, "devel", "*"))
    buildsdata = {'production': prodBuildDirs, 'devel': develBuildDirs}
    return buildsdata

class SWEnv(object):
    ''' Software environment object - categorize based on path and create module files '''

    def __init__(self, path, pathtype, modulerootpath, addtypelevel):
        self.path = path
        self.pathtype = pathtype
        self.modulerootpath = os.path.join(modulerootpath, "swenv")
        self.addtypelevel = addtypelevel
        self.categorize()

    def categorize(self):
        ''' Extract data from the SWEnv's path to categorize it and generate module paths '''
        if self.pathtype == 'production':
            self.buildtype = self.path.split('/')[-3]                    # production or (future) production-$arch
            self.swset = self.path.split('/')[-1]                        # default, bioinfo, ...
            self.buildroot = os.path.dirname(self.path)                  # path without swset (default, bioinfo, ...)
            self.versionstamp = self.path.split('/')[-2]                 # v0.1-20170602
            self.datestamp = self.versionstamp.split('-')[1]             # 20170602
            self.year = time.strptime(self.datestamp, "%Y%m%d").tm_year  # 2017
            if self.addtypelevel: buildtype = self.buildtype
            else: buildtype = ''
            self.modulepaths = [
                #os.path.join(self.modulerootpath, str(self.year), buildtype, self.versionstamp, "%s.lua" % self.swset),
                os.path.join(self.modulerootpath, buildtype, "%s-env" % self.swset, "%s.lua" % self.versionstamp),
            ]
        elif self.pathtype == 'devel':
            self.buildtype = self.path.split('/')[-2]                    # devel or (future) devel type
            self.swset = self.path.split('/')[-1]                        # default, bioinfo, ...
            self.buildroot = os.path.dirname(self.path)                  # path without swset (default, bioinfo, ...)
            mtime = datetime.datetime.fromtimestamp(os.stat(self.path).st_mtime)
            self.versionstamp = mtime.strftime('rolling-%Y%m%d')         # rolling-20170602
            self.datestamp = mtime.strftime('%Y%m%d')                    # 20170602
            self.year = mtime.year                                       # 2017
            self.modulepaths = [
                 #os.path.join(self.modulerootpath, self.buildtype, self.swset, "%s.lua" % self.versionstamp),
                 os.path.join(self.modulerootpath, self.buildtype, "%s-env.lua" % self.swset)
            ]
        else: raise Exception("Internal error - don't know how to handle path type %s." % self.pathtype)

    def generateModules(self, noop):
        ''' Create Lua module files from template '''
        env = jinja2.Environment(loader=jinja2.PackageLoader('resif', os.path.join('templates','modules')))
        template = env.get_template("%s.lua" % self.buildtype)
        for modulepath in self.modulepaths:
            if not noop:
                try:
                    os.makedirs(os.path.dirname(modulepath))
                except OSError as error:
                    if error.errno != errno.EEXIST: raise
            module = template.stream(vars(self))
            click.echo("==== Creating module for %s/%s: %s" % (self.versionstamp, self.swset, modulepath))
            if not noop:
                if os.path.exists(modulepath):
                    click.echo("Found existing module file, this shouldn't happen, stopping.", err=True)
                    exit(50)
                else: module.dump(modulepath)

    @staticmethod
    def prioritizeModules(swenvlist):
        ''' Decide which software environment is the latest and set special module paths for it  '''
        latest = sorted(filter(lambda el: el.pathtype == 'production', swenvlist), reverse=False).pop()
        for swenv in swenvlist:
            if swenv.pathtype == 'production' and swenv.buildroot == latest.buildroot:
                click.echo("==== Chosen as priority: %s" % swenv)
                swenv.modulepaths.append(os.path.join(swenv.modulerootpath, "%s-env" % swenv.swset, "latest.lua"))

    def __lt__(self, other):
        ''' Implement __lt__ so we can use sort/sorted on lists of SWEnv '''
        return LooseVersion(self.versionstamp) < LooseVersion(other.versionstamp) 

    def __str__(self):
        ''' Implement __str__ so we can print() a SWEnv '''
        return "%s : %s" % (self.__class__, self.path) # vars(self)

    def __repr__(self):
        ''' Implement __repr__ for SWEnv in case we want to reproduce it '''
        return ("%s('%s','%s','%s')" % (self.__class__.__name__, self.path, self.pathtype, self.modulerootpath))

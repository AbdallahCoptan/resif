#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage software set configuration files (resifile)
#######################################################################################################################

import os
import yaml
import glob
import re
import click
import source

# Get the list of software sets in a resifile
def getSoftwareSets (resifile):
    f = open(resifile, 'r')
    data = yaml.load(f)
    f.close()

    swsets = []

    for swset in data.keys():
        # Everything that is not toolchains or sources should be a swset
        if swset not in ['toolchains', 'sources']:
            swsets.append(swset)

    return swsets

# Check if an easyconfig file exists
def checkEasyConfig (ebfile, ebpaths):
    found = False
    match = re.match("^([\w-]+)-(v?[\d\.-]+)-(\w+)-?([\d\w.]+)?(.*)\.eb", ebfile)
    swname = match.group(1)

    for path in ebpaths:
        p = os.path.join(path, swname[0].lower(), swname)
        if os.path.isdir(p) and ebfile in os.listdir(p):
            found = True
    return found

# Look for similar easyconfigs (same toolchain, same year)
def findSimilarEasyConfig (ebfile, ebpaths):

    match = re.match("^([\w-]+)-(v?[\d\.-]+)-(\w+)-?([\d\w.]+)?(.*)\.eb", ebfile)

    if match:
        swname = match.group(1)
        swversion = match.group(2)
        toolchain = match.group(3)
        toolchainversion = match.group(4)
    else:
        return None

    if match.group(5):
        versionsuffix = match.group(5)
    else:
        versionsuffix = None

    # extract the year from the toolchainversion, if it's a year-based version
    match = re.match("^20[0-9]{2}", toolchainversion)

    # search in all easyconfig directories for similar files
    # also make sure that an easyconfig file for the original toolchain is present
    alternatives = []
    tceasyconfigs = []
    if match:
        if versionsuffix:
            search = "%s-%s-%s-%s*%s.eb" % (swname, swversion, toolchain, match.group(0), versionsuffix)
        else:
            search = "%s-%s-%s-%s*.eb" % (swname, swversion, toolchain, match.group(0))
        searchtc = "%s-%s.eb" % (toolchain, toolchainversion)
        for path in ebpaths:
            alternatives += glob.glob(os.path.join(path, swname[0].lower(), swname, search))
            tceasyconfigs += glob.glob(os.path.join(path, toolchain[0].lower(), toolchain, searchtc))

    if alternatives and tceasyconfigs:
        # just use the filename, also enables proper sorting
        alternatives = map(os.path.basename, alternatives)
        alternatives.sort(reverse=True)
        return alternatives[0]
    else:
        return None

# Determine from which easyconfig file to build the software
def getEasyConfig(ebfile, ebpaths):

    swhash = {}

    # if an easyconfig file exists for the specific software and toolchain version, use it
    if checkEasyConfig(ebfile, ebpaths):
        swhash['ebfile'] = ebfile
    # otherwise try to find similar easyconfig files
    else:
        sim = findSimilarEasyConfig(ebfile, ebpaths)
        if sim:
            toolchain, toolchainversion = ebfile[:-3].split("-")[2:4]
            swhash['ebfile'] = sim
            swhash['try'] = "%s,%s" % (toolchain, toolchainversion)
        # if no similar easyconfig files are found, we cannot build the software
        else:
            swhash['ebfile'] = None

    return swhash


# Get a hash with information from which easyconfig files to build the softwares in a specific software set
# and whether to try with a different toolchain
def getSoftwares(resifile, swsetname, ebpaths):

    ebpathslist = ebpaths.split(":")

    f = open(resifile, 'r')
    data = yaml.load(f)
    f.close()

    swsethash = {}

    for swset in data.keys():
        if swset == swsetname:
            # For each item in the list of software
            for sw in data[swset]:
                # If the list item is already a full .eb file specification
                # we can directly get the easyconfig file for it
                if sw.endswith(".eb"):
                    swsethash[sw[:-3]] = getEasyConfig(sw, ebpathslist)

                # If the list item is in the form of <software>/<version>-<versionsuffix>, we need to expand it with all
                # defined toolchains
                else:
                    slashsplit = sw.split('/')
                    # make sure we have at least <software>/<version>
                    if len(slashsplit) == 2:
                        name = slashsplit[0]
                        version = slashsplit[1]

                        # check for a versionsuffix
                        minussplit = version.split('-')
                        if len(minussplit) >= 2:
                            version = minussplit[0]
                            versionsuffix = "-".join(minussplit[1:])
                            for toolchain in data['toolchains']:
                                try:
                                    tcname, tcversion = toolchain.split("/")
                                except ValueError:
                                    click.secho("Error: '%s' is not a valid toolchain definition." % toolchain, err=True, fg='yellow')
                                    raise click.Abort
                                ebfile = "%s-%s-%s-%s-%s.eb" % (name, version, tcname, tcversion, versionsuffix)
                                swsethash[ebfile[:-3]] = getEasyConfig(ebfile, ebpathslist)
                        else:
                            for toolchain in data['toolchains']:
                                try:
                                    tcname, tcversion = toolchain.split("/")
                                except ValueError:
                                    click.secho("Error: '%s' is not a valid toolchain definition." % toolchain, err=True, fg='yellow')
                                    raise click.Abort
                                ebfile = "%s-%s-%s-%s.eb" % (name, version, tcname, tcversion)
                                swsethash[ebfile[:-3]] = getEasyConfig(ebfile, ebpathslist)
                    else:
                        click.secho("Error: '%s' is not a valid software definition." % sw, err=True, fg='yellow')
                        raise click.Abort

    return swsethash


def listSoftwareSets(configdir):
    for f in os.listdir(os.path.join(configdir, "swsets")):
        name, ext = os.path.splitext(f)
        if ext == ".yaml":
            click.echo("%s" % name)
    return


def info(resifile):

    f = open(resifile, 'r')
    click.echo(f.read())
    f.close()

    return


def add(name, configdir):
    data = {}

    if click.confirm("Do you want to specify sources specific for this software set?"):
        data['sources'] = {}
        sourcename = click.prompt("Please give a name for the source")
        data['sources'][sourcename] = source.__collectInfo()

        while click.confirm("Do you want to specifiy another source?"):
            sourcename = click.prompt("Please give a name for the source")
            data['sources'][sourcename] = source.__collectInfo()

    if click.confirm("Do you want to specify toolchains?"):
        data['toolchains'] = []
        click.echo("Please enter the toolchains one per line in the format <name>/<version>, and finish with an empty line.")
        tc = raw_input()
        while tc:
            data['toolchains'].append(tc)
            tc = raw_input()

    data[name] = []
    click.echo("Please enter the softwares one per line in the format <name>-<version>-<toolchain>.eb or <name>/<version> if you have defined toolchains, and finish with an empty line.")
    sw = raw_input()
    while sw:
        data[name].append(sw)
        sw = raw_input()

    filename = os.path.join(configdir, "swsets", "%s.yaml" % (name))
    f = open(filename, 'w')
    yaml.safe_dump(data, f, default_flow_style=False)
    f.close()
    click.echo("Software set successfully created.")


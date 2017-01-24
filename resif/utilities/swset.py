#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage software set configuration files (resifile)
#######################################################################################################################

import os
import yaml
import glob
import re

# Get a list of lists of .eb filenames (list of software sets) from a resifile
def getSoftwareLists (resifile):
    f = open(resifile, 'r')
    data = yaml.load(f)
    f.close()

    swsets = {}

    for swset in data.keys():
        # Everything that is not toolchains or sources should be a swset
        if swset not in ['toolchains', 'sources']:
            swlist = []
            # For each item in the list of software
            for sw in data[swset]:
                # If the list item is already a full .eb file, we just add it to the final list
                if sw.endswith(".eb"):
                    swlist.append(sw)
                # If the list item is in the form of <software>/<version>, we need to expand it with all defined
                # toolchains to a full .eb filename
                else:
                    name, version = sw.split('/')
                    for toolchain in data['toolchains']:
                        tcname, tcversion = toolchain.split("/")
                        ebfile = "%s-%s-%s-%s.eb" % (name, version, tcname, tcversion)
                        swlist.append(ebfile)
            swsets[swset] = swlist

    return swsets

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
    swname = ebfile.split("-")[0]

    for path in ebpaths:
        if ebfile in os.listdir(os.path.join(path, swname[0].lower(), swname)):
            found = True
    return found

# Look for similar easyconfigs (same toolchain, same year)
def findSimilarEasyConfig (ebfile, ebpaths):
    swname, swversion, toolchain, toolchainversion = ebfile.split("-")
    toolchainversion = toolchainversion[:-3]

    # extract the year from the toolchainversion, if it's a year-based version
    match = re.match("^20[0-9]{2}", toolchainversion)

    # search in all easyconfig directories for similar files
    alternatives = []
    if match:
        search = "%s-%s-%s-%s*.eb" % (swname, swversion, toolchain, match.group(0))
        for path in ebpaths:
            alternatives += glob.glob(os.path.join(path, swname[0].lower(), swname, search))

    if alternatives:
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
            toolchain, toolchainversion = ebfile[:-3].split("-")[2:]
            swhash['ebfile'] = sim
            swhash['try'] = "%s,%s" % (toolchain, toolchainversion)
        # if no similar easyconfig files are found, we cannot build the software
        else:
            swhash['ebfile'] = None

    return swhash


# Get a hash with information from which easyconfig files to build the softwares in a specific software set
# and whether to try with a different toolchain
def getSoftwareLists (resifile, swsetname, ebpaths):

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

                # If the list item is in the form of <software>/<version>, we need to expand it with all defined
                # toolchains
                else:
                    name, version = sw.split('/')
                    for toolchain in data['toolchains']:
                        tcname, tcversion = toolchain.split("/")
                        ebfile = "%s-%s-%s-%s.eb" % (name, version, tcname, tcversion)
                        swsethash[ebfile[:-3]] = getEasyConfig(ebfile, ebpathslist)

    return swsethash


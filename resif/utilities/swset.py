#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage software set configuration files (resifile)
#######################################################################################################################

import os
import yaml

# Create default software set with HPL-2.2-foss-2016.09
def createDefaultSwset(params):
    filename = "default.yaml"
    data = {'default': ['HPL/2.2'], 'toolchains': ['foss/2016.09']}
    comment = """# swsets/default.yaml
# Default RESIF software set -- set by 'resif init'
###############################
# Default Toolchains to Build #
###############################
# get the list of  supported compiler toolchains using:
#      eb --list-toolchains
# See also http://easybuild.readthedocs.io/en/latest/eb_list_toolchains.html\n"""

    f = open(os.path.join(params["configdir"], "swsets", filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()

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


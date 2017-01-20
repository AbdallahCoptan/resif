#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage role configuration files
#######################################################################################################################

import os
import yaml

# Get variables from a role
def get(name, configdir):
    filename = os.path.join(configdir, "roles", name + ".yaml")

    f = open(filename, 'r')
    data = yaml.load(f)
    f.close()

    return data
import os
import yaml

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

def getSoftwareLists (resifile):
    f = open(resifile, 'r')
    data = yaml.load(f)
    f.close()

    swsets = {}

    for swset in data.keys():
        if swset not in ['toolchains', 'sources']:
            swlist = []
            for sw in data[swset]:
                if sw.endswith(".eb"):
                    swlist.append(sw)
                else:
                    name, version = sw.split('/')
                    for toolchain in data['toolchains']:
                        tcname, tcversion = toolchain.split("/")
                        ebfile = "%s-%s-%s-%s.eb" % (name, version, tcname, tcversion)
                        swlist.append(ebfile)
            swsets[swset] = swlist

    return swsets


import os
import yaml
import getpass

def createDefaultRole(params):
    filename = "default.yaml"
    data = {'user': getpass.getuser(),
            'resifile': str(os.path.join(params["configdir"], "swsets", "default.yaml")),
            'datadir': str(params["datadir"]),
            'mns': params["mns"],
            'swset': 'default',
            'buildmode': 'local'
            }
    comment = "# roles/default.yaml\n# Default RESIF user role -- set by 'resif init'\n"

    f = open(os.path.join(params["configdir"], "roles", filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()

def get(name, configdir):
    filename = os.path.join(configdir, "roles", name + ".yaml")

    f = open(filename, 'r')
    data = yaml.load(f)
    f.close()

    return data
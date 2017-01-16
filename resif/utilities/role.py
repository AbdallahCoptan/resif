import os
import yaml
import getpass

def createDefaultRole(params):
    filename = "default.yaml"
    data = {'user': getpass.getuser(),
            'resifile': str(os.path.join(params["configdir"], "swsets", "default.yaml")),
            'datadir': str(params["datadir"]),
            'mns': 'categorized_mns',
            'swset': 'default',
            'buildmode': 'local'
            }
    comment = "# roles/default.yaml\n# Default RESIF user role -- set by 'resif init'\n"

    f = open(os.path.join(params["configdir"], "roles", filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()
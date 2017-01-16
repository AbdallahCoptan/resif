import os
import yaml

def createDefaultSource(path):
    filename = "default.yaml"
    data = {'priority': 50, 'easyconfigs': {'git': 'https://github.com/hpcugent/easybuild-easyconfigs'}, 'easyblocks': {'git': 'https://github.com/hpcugent/easybuild-easyblocks'}}
    comment = "# sources/default.yaml\n# Default RESIF EB sources -- set by 'resif init'\n"

    f = open(os.path.join(path, filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()
import os
import yaml
import sys
from git import Repo

def createDefaultSource(params):
    filename = "default.yaml"
    data = {'priority': 50, 'easyconfigs': {'git': 'https://github.com/hpcugent/easybuild-easyconfigs'}, 'easyblocks': {'git': 'https://github.com/hpcugent/easybuild-easyblocks'}}
    comment = "# sources/default.yaml\n# Default RESIF EB sources -- set by 'resif init'\n"

    f = open(os.path.join(params["configdir"], "sources", filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()

def __pull(repoinfo, path):
    if "path" in repoinfo:
        if not os.path.isdir(path):
            os.symlink(repoinfo["path"], path)

    elif "git" in repoinfo:
        if os.path.isdir(path):
            repo = Repo(path)
        else:
            repo = Repo.clone_from(repoinfo["git"], path)

        # If a a branch or a release has been given, we change the state of the repository accordingly, if not, we use the default branch
        git = repo.git()
        git.fetch("--all", "--tags", "--prune")

        if 'tag' in repoinfo:
            git.checkout("tags/%s" % (repoinfo['tag']))
        elif 'branch' in repoinfo:
            git.checkout(repoinfo['branch'])
        elif 'ref' in repoinfo:
            git.checkout(repoinfo['ref'])
        elif 'commit' in repoinfo:
            git.checkout(repoinfo['commit'])


def pullall(configdir, datadir):
    sources_config_path = os.path.join(configdir, "sources")
    for sourcefile in os.listdir(sources_config_path):
        print(sourcefile)
        name = sourcefile.rstrip(".yaml")
        print(name)
        eblockspath = os.path.join(datadir, "easyblocks", name)
        ebconfigspath = os.path.join(datadir, "easyconfigs", name)

        f = open(os.path.join(sources_config_path, sourcefile), 'r')
        source = yaml.load(f)
        f.close()

        if "easyblocks" in source:
            __pull(source["easyblocks"], eblockspath)
        if "easyconfigs" in source:
            __pull(source["easyconfigs"], ebconfigspath)

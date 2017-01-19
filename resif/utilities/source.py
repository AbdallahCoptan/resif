#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage easyconfig and easyblocks sources and their configuration files
#######################################################################################################################

import os
import yaml

from git import Repo

# Create default configuration with the repositories from hpcugent
def createDefaultSource(params):
    filename = "default.yaml"
    data = {'priority': 50, 'easyconfigs': {'git': 'https://github.com/hpcugent/easybuild-easyconfigs'}, 'easyblocks': {'git': 'https://github.com/hpcugent/easybuild-easyblocks'}}
    comment = "# sources/default.yaml\n# Default RESIF EB sources -- set by 'resif init'\n"

    f = open(os.path.join(params["configdir"], "sources", filename), 'w')
    f.write(comment)
    yaml.dump(data, f, default_flow_style=False)
    f.close()

# Pull/update a repository with the specified branch, commit, tag or ref
# or just do a symlink if it's a local path
def __pull(repoinfo, path):
    # If path is specified, just do a symlink
    if "path" in repoinfo:
        if not os.path.isdir(path):
            os.symlink(repoinfo["path"], path)

    # If it's a git repository
    elif "git" in repoinfo:
        # if it's already present, just init the Repo object with the path
        if os.path.isdir(path):
            repo = Repo(path)
        # Otherwise clone the repo
        else:
            repo = Repo.clone_from(repoinfo["git"], path)

        # If a a branch or a release has been given, we change the state of the repository accordingly, if not, we use the default branch
        git = repo.git()
        git.fetch("--all", "--tags", "--prune")

        if 'tag' in repoinfo:
            git.checkout("tags/%s" % (repoinfo['tag']))
        elif 'branch' in repoinfo:
            git.checkout(repoinfo['branch'])
            git.pull()
        elif 'ref' in repoinfo:
            git.checkout(repoinfo['ref'])
        elif 'commit' in repoinfo:
            git.checkout(repoinfo['commit'])
        else:
            git.pull()


# Pull/update all sources defined in the config directory and from the optional resifile
# and return their local paths
def pullall(configdir, datadir, resifile=None):

    eblockspathslist = []
    econfigspathslist = []

    sources_config_path = os.path.join(configdir, "sources")

    # Pull/update all sources in the configuration directory
    for sourcefile in os.listdir(sources_config_path):
        name = sourcefile.rstrip(".yaml")

        # Paths to the repo are <datadir>/easy{blocks,configs}/<sourcename>
        eblockspath = os.path.join(datadir, "easyblocks", name)
        econfigspath = os.path.join(datadir, "easyconfigs", name)

        f = open(os.path.join(sources_config_path, sourcefile), 'r')
        source = yaml.load(f)
        f.close()

        if "easyblocks" in source:
            __pull(source["easyblocks"], eblockspath)
            eblockspathslist.append((source['priority'],eblockspath))
        if "easyconfigs" in source:
            __pull(source["easyconfigs"], econfigspath)
            econfigspathslist.append((source['priority'], os.path.join(econfigspath, "easybuild", "easyconfigs")))

    if resifile:
        f = open(resifile, 'r')
        data = yaml.load(f)
        f.close()

        # Check if sources are definied in the resifile
        if 'sources' in data:
            for name in data['sources'].keys():
                eblockspath = os.path.join(datadir, "easyblocks", name)
                econfigspath = os.path.join(datadir, "easyconfigs", name)
                source = data['sources'][name]

                if "easyblocks" in source:
                    __pull(source["easyblocks"], eblockspath)
                    eblockspathslist.append((source['priority'], eblockspath))
                if "easyconfigs" in source:
                    __pull(source["easyconfigs"], econfigspath)
                    econfigspathslist.append((source['priority'], os.path.join(econfigspath, "easybuild", "easyconfigs")))

    # Sort the paths by their priority
    eblockspathslist.sort(key=lambda x: x[0])
    econfigspathslist.sort(key=lambda x: x[0])

    # Return the lists of paths separated by :
    return (":".join(map(lambda x: x[1], eblockspathslist)), ":".join(map(lambda x: x[1], econfigspathslist)))

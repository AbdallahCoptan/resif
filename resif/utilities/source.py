import os
import yaml

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
            git.pull()
        elif 'ref' in repoinfo:
            git.checkout(repoinfo['ref'])
        elif 'commit' in repoinfo:
            git.checkout(repoinfo['commit'])
        else:
            git.pull()



def pullall(configdir, datadir, additional_sources=None):

    eblockspathslist = []
    econfigspathslist = []

    sources_config_path = os.path.join(configdir, "sources")

    for sourcefile in os.listdir(sources_config_path):
        name = sourcefile.rstrip(".yaml")
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
            econfigspathslist.append((source['priority'], econfigspath))

    if additional_sources:
        for name in additional_sources.keys():
            eblockspath = os.path.join(datadir, "easyblocks", name)
            econfigspath = os.path.join(datadir, "easyconfigs", name)
            source = additional_sources[name]

            if "easyblocks" in source:
                __pull(source["easyblocks"], eblockspath)
                eblockspathslist.append((source['priority'], eblockspath))
            if "easyconfigs" in source:
                __pull(source["easyconfigs"], econfigspath)
                econfigspathslist.append((source['priority'], econfigspath))

    eblockspathslist.sort(key=lambda x: x[0])
    econfigspathslist.sort(key=lambda x: x[0])

    return (":".join(map(lambda x: x[1], eblockspathslist)), ":".join(map(lambda x: x[1], econfigspathslist)))

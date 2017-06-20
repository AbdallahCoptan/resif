#######################################################################################################################
# Author: Sarah Diehl
# Mail: hpc-sysadmins@uni.lu
# Overview: Manage easyconfig and easyblocks sources and their configuration files
#######################################################################################################################

import os
import yaml
import click

from git import Repo

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
def pullall(configdir, datadir, additional_sources={}):

    eblockspathslist = []
    econfigspathslist = []

    all_sources = {}

    sources_config_path = os.path.join(configdir, "sources")

    # Collect all sources from configdir/sources/
    for sourcefile in os.listdir(sources_config_path):
        name = sourcefile.rstrip(".yaml")

        f = open(os.path.join(sources_config_path, sourcefile), 'r')
        source = yaml.load(f)
        f.close()

        all_sources[name] = source

    # Add additional_sources
    # additional_sources overwrite default sources if the name is identical
    all_sources.update(additional_sources)

    # Generate paths and pull (if git) all sources
    for name in all_sources.keys():

        source = all_sources[name]

        if "easyblocks" in source:
            eblockspath = os.path.join(datadir, "easyblocks", name)
            __pull(source["easyblocks"], eblockspath)

            if 'directory' in source['easyblocks']:
                eblockspath = os.path.join(eblockspath, source['easyblocks']['directory'])

            eblockspathslist.append((source['priority'], eblockspath))

        if "easyconfigs" in source:

            econfigspath = os.path.join(datadir, "easyconfigs", name)
            __pull(source["easyconfigs"], econfigspath)

            if 'directory' in source['easyconfigs']:
                econfigspath = os.path.join(econfigspath, source['easyconfigs']['directory'])

            if os.path.isdir(os.path.join(econfigspath, "easybuild", "easyconfigs")):
                econfigspathslist.append(
                    (source['priority'], os.path.join(econfigspath, "easybuild", "easyconfigs")))
            else:
                econfigspathslist.append((source['priority'], econfigspath))

    # Sort the paths by their priority
    eblockspathslist.sort(key=lambda x: x[0])
    econfigspathslist.sort(key=lambda x: x[0])

    # Return the lists of paths separated by :
    return (":".join(map(lambda x: x[1], eblockspathslist)),
            ":".join(map(lambda x: x[1], econfigspathslist)))


def list(configdir):
    for f in os.listdir(os.path.join(configdir, "sources")):
        click.echo(os.path.splitext(f)[0])


def remove(name, configdir):
    filename = os.path.join(configdir, "sources", "%s.yaml" % (name))
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        click.echo("Could not find source \"%s\" in %s." % (name,configdir), err=True)


def info(name, configdir):
    filename = os.path.join(configdir, "sources", "%s.yaml" % (name))
    if os.path.isfile(filename):
        f = open(filename, 'r')
        click.echo(f.read())
        f.close()
    else:
        click.echo("Could not find source \"%s\" in %s." % (name, configdir), err=True)


def __collectSourceInfo():
    data = {}
    typ = click.prompt("Specify the source type (local|git)", type=click.Choice(['local', 'git']), default="git")
    if typ == "local":
        data['path'] = click.prompt("Specify a local path")
        while not os.path.isdir(os.path.abspath(os.path.expandvars(data['path']))):
            click.echo("Invalid path!", err=True)
            data['path'] = click.prompt("Specify a local path")
    elif typ == "git":
        data['git'] = click.prompt("Specify the git URL")
        if click.confirm("Do you want to specify a specific branch, tag, ref or commit?"):
            spec = click.prompt("What do you want to specify (branch|tag|ref|commit)?", type=click.Choice(['branch', 'ref', 'tag', 'commit']))
            data[spec] = click.prompt("Specify the value")
    return data

def __collectInfo():
    data = {}

    data['priority'] = click.prompt('Specify a priority', default=100)
    if click.confirm("Do you want to add an easyconfig source?"):
        data['easyconfigs'] = __collectSourceInfo()
    if click.confirm("Do you want to add an easyblocks source?"):
        data['easyblocks'] = __collectSourceInfo()
    if not 'easyconfigs' in data and not 'easyblocks' in data:
        click.echo("You need to specify an easyconfigs or easyblocks source.", err=True)
        raise click.Abort

    return data

def add(name, configdir):
    filename = os.path.join(configdir, "sources", "%s.yaml" % (name))
    if os.path.isfile(filename):
        click.echo("Source already exists.", err=True)
        exit(50)
    else:
        data = __collectInfo()
        if data:
            f = open(filename, 'w')
            yaml.safe_dump(data, f, default_flow_style=False)
            f.close()
            click.echo("Source successfully created.")
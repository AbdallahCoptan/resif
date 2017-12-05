-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Fri 2017-01-13 08:55 svarrette>

RESIF relies on [Easybuild](https://hpcugent.github.io/easybuild) recipes to install the softwares listed within [software sets](software_sets.md).
Default [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) comes from the official EB Github repository, _i.e_:

* [easybuild-easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs)
* [easybuild-easyblocks](https://github.com/hpcugent/easybuild-easyblocks)

You might wish to configure for some of the software you wish to install your custom source for these repository, _i.e._

* your (private) fork of these repository holding your customized recipes
* your local copy of these repository your working on when developing your own recipes

## YAML Format for EB sources

You are free to give to each of these [custom] sources a short name `<shortname>` (except `default`) you can refer to later when listing the eb files to build.
To do that, set a file `<configdir>/sources/<shortname>.yaml` according to the following format:

~~~yaml
# <shortname>.yaml
# Specification of custom EasyBuild source repositories

priority: <n>   # Default source get priority 100
easyconfigs:    # Specification for easybuild-easyconfigs
  path: "/path/to/easybuild-easyconfigs" # local path
  git:  "<giturl>"            # OR (better) git url for the repository
  ref:  "<ref>"               # (optional) git object that should be checked out.
  tag:  "<tag>"               # (optional) git tag that should be checked out
  commit: "<commit>"          # (optional) a specific git commit
  branch: "<branch>"          # (optional) a specific branch to pull
  directory: "<subdirectory>" # (optional) define a subdirectory to be used as the root directory
easyblocks:    # Specification for easybuild-easyblocks
  path: "/path/to/easybuild-easyblocks" # local path
  git:  "<giturl>"            # OR (better) git url for the repository
  ref:  "<ref>"               # (optional) git object that should be checked out.
  tag:  "<tag>"               # (optional) git tag that should be checked out
  commit: "<commit>"          # (optional) a specific git commit
  branch: "<branch>"          # (optional) a specific branch to pull
  directory: "<subdirectory>" # (optional) define a subdirectory to be used as the root directory
~~~

Typically, you will end with the following layout:

```bash
<configdir>
└── sources     # Easybuild sources
    ├── default.yaml   # default easybuild repositories
    ├── ulhpc.yaml
    └── local.yaml
```

Where these files are defines as follows:

~~~yaml
# sources/default.yaml
# Default RESIF EB sources -- set by 'resif init'

priority: 50
easyconfigs:
  git: "https://github.com/hpcugent/easybuild-easyconfigs"
easyblocks:
  git: "https://github.com/hpcugent/easybuild-easyblocks"
~~~

~~~yaml
# sources/local.yaml
# RESIF custom EB sources -- set your local working directories
# Note: use default easyblocks as not precised here

priority: 75
easyconfigs:
  path: "$HOME/devel/easybuild/easyconfigs"
~~~

~~~yaml
# sources/ulhpc.yaml
# RESIF custom EB sources -- use ULHPC forks

priority: 1
easyconfigs:
  git: "https://github.com/ULHPC/easybuild-easyconfigs"
  branch: 'uni.lu'
easyblocks:
  git: "https://github.com/ULHPC/easybuild-easyblocks"
~~~

In particular, the above setting means that when a given `<software>.eb` recipe is to be built, RESIF will search for it in the following order:

1. in the `<ulhpc>` sources (priority:1)
2. the default sources (priority: 50)
3. the `local` sources (priority: 75)

## Resulting Directory Layout

The specification of EB sources impact all `resif` actions as the defined repositories need to be cloned/updated under the RESIF `<datadir>` (_i.e._ `~/.local/resif` by default, see [variables.md](variables.md)).
To easily switch from one source to another, RESIF will setup the repository `easy{configs,blocks}` for the source `<name>` under `<datadir>/easy{configs,blocks}/<name>/`.
In particular, with the above configuration (_i.e._ `<configdir>/sources/{default,local,ulhpc}.yaml`):

```bash
<datadir>
├── easyblocks
│   ├── default/      # default easyblocks sources i.e. git from hpcugent/easybuild-easyblocks
│   │   ├── CONTRIBUTING.md
│   │   └── [...]
│   ├── ulhpc/ # custom easyblocks sources  from ULHPC/easybuild-easyblocks fork
│   │   ├── CONTRIBUTING.md
│   │   └── [...]
│   └── local -> /path/to/local/easyblocks  # Local symlink to the path
└── easyconfigs     # default easyconfig sources i.e. git from hpcugent/easybuild-easyblocks
    ├── default/
    │   ├── CONTRIBUTING.md
    │   └── [...]
    ├── ulhpc_github/
    │   ├── CONTRIBUTING.md
    │   └── [...]
    └── local -> /path/to/local/easyconfigs
```

Note that _a priori_, `<datadir>` also hosts the generated software and modules such that the complete layout of this directory includes additional directories as depicted in [`variables.md`](variables.md), section `<datadir>`

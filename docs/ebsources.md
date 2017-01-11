-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 16:15 svarrette>

RESIF relies on [Easybuild](https://hpcugent.github.io/easybuild) recipes to install the softwares listed within [software sets](software_sets.md).
Default [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) comes from the official EB Github repository, _i.e_:

* [easybuild-easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs)
* [easybuild-easyblocks](https://github.com/hpcugent/easybuild-easyblocks)

You might wish to configure for some of the software you wish to install your custom source for these repository, _i.e._

* your (private) fork of these repository holding your customized recipes
* your local copy of these repository your working on when developing your own recipes

You are free to give to each of these [custom] sources a short name `<shortname>` (except `default`) you can refer to later when listing the eb files to build.
To do that, set a file `<configdir>/sources/<shortname>.yaml` according to the following format:

~~~yaml
# <shortname>.yaml
# Specification of custom EasyBuild source repositories

priority: <n>   # Default source get priority 100
easyconfigs:    # Specification for easybuild-easyconfigs
  path: "/path/to/easybuild-easyconfigs" # local path
  git:  "<giturl>"     # OR (better) git url for the repository
  ref:  "<ref>"        # (optional) git object that should be checked out.
  tag:  "<tag>"        # (optional) git tag that should be checked out
  commit: "<commit>"   # (optional) a specific git commit
  branch: "<branch>"   # (optional) a specific branch to pull
easyblocks:    # Specification for easybuild-easyblocks
  path: "/path/to/easybuild-easyblocks" # local path
  git:  "<giturl>"     # OR (better) git url for the repository
  ref:  "<ref>"        # (optional) git object that should be checked out.
  tag:  "<tag>"        # (optional) git tag that should be checked out
  commit: "<commit>"   # (optional) a specific git commit
  branch: "<branch>"   # (optional) a specific branch to pull
~~~

Typically, you will end with the following layout:

```bash
<configdir>
└── sources     # Easybuild sources
    ├── default.yaml   # default settings, based on
    ├── ulhpc.yaml
    └── local.yaml
```

Where these files are defines as follows:

~~~yaml
# sources/default.yaml
# Default RESIF EB sources -- set by 'resif init'

priority: 50
easyconfigs:
  git: https://github.com/hpcugent/easybuild-easyconfigs
easyblocks:
  git: https://github.com/hpcugent/easybuild-easyblocks
~~~

~~~yaml
# sources/local.yaml
# RESIF custom EB sources -- se your local working directories

priority: 75
easyconfigs:
  path: "$HOME/devel/easybuild/easyconfigs"
# Note: use default easyblocks from
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

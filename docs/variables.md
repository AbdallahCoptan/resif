
        Time-stamp: <Fri 2017-01-13 09:00 svarrette>

--------------------------
## RESIF Variables Overview

The workflow revolves around a few variables that are defined below.
Although it is interesting to take a look at them to personalize an installation, `resif` can be used without manually setting any of these options since the necessary ones have a (hopefully meaningfull) default value.

Here are all the __RESIF__ variables that can be set, followed by their descriptions.

| RESIF Variable | Description                                                                                                | Default (if any)                          |
|----------------|------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| `group`        | Group that will own `<installdir>`                                                                         |                                           |
| `configdir`    | Configuration directory                                                                                    | `$HOME/.config/resif/`                    |
| `resifile`     | RESIF file to use, defining the software set__s__ to deploy                                                | `<configdir>/swsets/default.yaml`         |
| `datadir`      | Local Data directory                                                                                       | `$HOME/.local/resif/`                     |
| `mns`          | Module Naming Scheme (see [`mns.md`](mns.md))                                                              | `categorized_mns`                         |
| `version`      | Current version to deploy, under the form `<major>.<minor>.<patch>` (see [`versioning.md`](versioning.md)) | content of `<configdir>/VERSION`          |
| `swset`        | Current Software set to deploy (from `<resifile>`)                                                         | `default`                                 |
| `release`      | Current _general_ release of the RESIF deployment (__differs__ from Resif version)                         | `v<major>.<minor>`                        |
| `releasedir`   | Subdirectory in which a release is to be deployed                                                          | `[branch/]<release>-<date>` OR `<branch>` |
| `installdir`   | Root Installation directory (__differs__ from `eb_installpath`, see [`versioning.md`](versioning.md))      | `<datadir>/<releasedir>/<swset>`          |
| `buildmode`    | Local build ('local') vs. via job submission  ('job')                                                      | local                                     |
| `eb_options`   | String of options to pass "as is" to EasyBuild.                                                            |                                           |



Note that for some of the above variables, the corresponding environmental variable `$RESIF_<uppercase(variable)>` can be set (see `resif --help` and `resif <command> --help` for details).

Thus configuring RESIF can be done:

* using `resif` with command line arguments
* setting environment variables (`$RESIF_...`)
* providing one or more role configuration files

The order of preference for the different configuration types is as listed above, that is:

1. EasyBuild default values (if applicable)
2. values in the role configuration file
3. environment variables override the corresponding entries in the role configuration file
4. command line arguments in turn override the corresponding environment variables and matching entries in the role configuration file

In addition, as RESIF interacts with [Easybuild](https://hpcugent.github.io/easybuild), it sets several variables (prefixed with `eb_`) of interest for Easybuild that are listed below

| RESIF Variable   | Easybuild equivalent      | Description                                                                      | Default (if any)         |
|------------------|---------------------------|----------------------------------------------------------------------------------|--------------------------|
| `eb_prefix`      | `$EASYBUILD_PREFIX`       | Prefix directory for Easybuild installation                                      | `$HOME/.local/easybuild` |
| `eb_module_tool` | `$EASYBUILD_MODULES_TOOL` | Module tool, in [ 'Lmod', 'Tcl']                                                 |                          |
| `eb_buildpath`   | `$EASYBUILD_BUILDPATH`    | (temporary) directories to host builds -- you may want `/dev/shm` here           | `<eb_prefix>/build`      |
| `eb_installpath` | `$EASYBUILD_INSTALLPATH`  | Root directory for installed software (`software/`) and modules (`modules/all/`) | `<eb_prefix>`            |


### `<group>`: Software group

* after building the software the group of the `<installdir>` will be changed to this group

### `<configdir>`: Configuration directory

The configuration directory for RESIF (__Default__: `$HOME/.config/resif/`), setup by `resif init` -- see [`cli/index.md`](cli/index.md)).
The typical layout of this directory is depicted below:

```bash
<configdir>
  ├── roles/   # RESIF roles, to alter the default variables depending on the deployment context
  │    ├── sysadmin.yaml  # HPC cluster sysadmin, expecting global deployment
  │    └── default.yaml   # default role settings, i.e. local user
  ├── sources/   # Easybuild sources
  │    └── default.yaml   # default settings, based on reference 'hpcugent' Github repositories
  └── swsets/          # YAML definitions for the software sets
       ├── ulhpc.yaml
       └── default.yaml   # default software set
```

### `<resifile>`: RESIF file

This YAML file is used to define the [software sets](software_sets.md) to deploy.
It thus serve as the main configuration file for RESIF as defined by default in `<configdir>/swsets/default.yaml`.

For more details on its format, see [`RESIFile.md`](RESIFile.md).

### `<datadir>`: Specific Data directory

The data directory for RESIF (__Default__: `$HOME/.local/resif/`), setup by `resif init` -- see [`cli/index.md`](cli/index.md)).
It will typically hold:

* the working copy(ies) of the Easybuild recipe repositories (_i.e._ [easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs) and [easyblocks](https://github.com/hpcugent/easybuild-easyblocks) used to install the software sets.
* the software sets (_i.e._ software and modules) built by RESIF according to a specific hierarchy -- see `<installdir>`.

The typical layout of this directory is depicted below:

```bash
<datadir>
├── devel/        # RESIF build as defined in the 'devel' branch of the resif-control repository
│   ├── default/      # 'default' software set
│   ├── fluent/       # (new) specific software set (for using the Fluent software suite)
│   ├── luxdem/       # specific software set (for the LuxDEM team)
│   └── stata/        # specific software set (for using the Stata software suite)
├── production/   # RESIF build as defined in the 'production' branch of the resif-control repository
│   ├── v0.9 -> v0.9-20141210    # Symbolic link for v0.9, to abstract from timestamp
│   ├── v1.0 -> v1.0-20150302    # Symbolic link for v1.0, to abstract from timestamp
│   ├── v1.1 -> v1.1-20150714    # Symbolic link for v1.1, to abstract from timestamp
│   ├── v0.9-20141210/   # released version 0.9, built in December, 2014
│   │   └── default/        # 'default' software set
│   ├── v1.0-20150302    # released version 1.0, built in March, 2015
│   │   ├── default/        # 'default' software set
│   │   └── luxdem/         # specific software set (for the LuxDEM team)
│   ├── v1.1-20150714    # released version 1.1, built in July, 2015
│   │   ├── default/        # 'default' software set
│   │   ├── luxdem/         # specific software set (for the LuxDEM team)
│   │   └── stata/          # specific software set (for using the Stata software suite)
│   └── last -> v1.1-20150714    # Symlink to the latest build sets
├── stable -> production/last  # Symlink to the latest stable release
├── testing -> devel
├── v0.9 -> production/v0.9
├── v1.0 -> production/v1.0
├── v1.1 -> production/v1.1
├── easyblocks
│   ├── default/      # default easyblocks sources i.e. git from hpcugent/easybuild-easyblocks
│   ├── ulhpc/        # custom easyblocks sources  from ULHPC/easybuild-easyblocks fork
│   └── local -> /path/to/local/easyblocks  # Local symlink to the path
└── easyconfigs
    ├── default/    # default easyconfig sources i.e. git from hpcugent/easybuild-easyconfigs
    ├── ulhpc/      # custom easyconfigs sources  from ULHPC/easybuild-easyconfigs fork
    └── local -> /path/to/local/easyconfigs
```

###  `<mns>`: Module Naming Scheme

See [`mns.md`](mns.md).


### `<release>`: Deployment Release Version

A [semantic versioning](http://semver.org/) approach is enforced for all RESIF deployment, the current version being stored on the `<configdir>/VERSION` file. In this context, a version number have the following format:

      <major>.<minor>.<patch>

Due to the [Deployment releasing policy](versioning.md), and for the sake of simplicity, **only the Major and Minor release lead to a new root directory (named v.X.Y) in the environment modules directory layout**.
In particular, any patch release `X.Y.Z` is applied into the existing `X.Y` environment modules hierarchy.

Thus, the `<release>` variable reflects this policy and only old the value `v<major>.<minor>` as extracted from `<configdir>/VERSION`.

### `<releasedir>`: Subdirectory for a release

For all deploying situations, we wish to reflect the RESIF context of the build (at least with a timestamp information).
So `<releasedir>` corresponds by default to `<release>-<timestamp>` (Ex: `v0.6-20170117`).

`/!\ IMPORTANT`: In addition, assuming `<configdir>` is a git repository (thus a `resif-control` repository) **and** is configured according to a  [gitflow](http://nvie.com/posts/a-successful-git-branching-model/) layout, you might wish to reflect the current branch / git context you are operating on.
This is of interest upon a __minor or major__ release, _i.e._ when a `git flow release` operation is performed within the *production-ready* branch (as obtained from `git config --get gitflow.branch.master`, thus corresponding typically to the `production` branch).
In this case, `<releasedir>` would be prefixed with the branch name of the resif-control repository and thus corresponds to `<branch>/<release>-<timestamp>`.
Ex: `production/v0.6-20170117`.
On the contrary, on the branch used for daily development (as obtained by ` git config --get gitflow.branch.develop`, thus corresponding typically to the `devel` or `master` branch), the timestamp or even the version has little interest, in which case it might be simpler to have `<releasedir>` corresponding to `<branch>`

This layout is reflected in the above example concerning `<datadir>`.



### `<buildmode>`: Build mode

The way the software package are built, _i.e._ either locally (`local`, __default__) or via job submission on the platform (`job`).

__NOTE:__ `job` build mode is not implemented yet!



### `<eb_options>`: Additional EB options

Use this variable to tweak the behavior of EasyBuild more in depth for options that are not supported directly by RESIF.
As an example to run the command as a "dry run":

~~~bash
$> resif build --eb-options "--dry-run" core
~~~

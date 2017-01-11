
        Time-stamp: <Wed 2017-01-11 23:28 svarrette>

--------------------------
## RESIF Variables Overview

The workflow revolves around a few variables that are defined below.
Although it is interesting to take a look at them to personalize an installation, `resif` can be used without manually setting any of these options since the necessary ones have a (hopefully meaningfull) default value.

Here are all the __RESIF__ variables that can be set, followed by their descriptions.

| RESIF Variable | Description                                                              | Default (if any)          |
|----------------|--------------------------------------------------------------------------|---------------------------|
| `user`         | User operating the process                                               | `<whoami>`                |
| `group`        | Group used for operating the process                                     |                           |
| `configdir`    | Configuration directory                                                  | `$HOME/.config/resif/`    |
| `datadir`      | Local Data directory                                                     | `$HOME/.local/resif/`     |
| `mns`          | Module Naming Scheme (see [`mns.md`](mns.md))                            | `categorized_mns`         |
| `release`      | Current release of the RESIF deployment (__differs__ from Resif version) | `v<major>.<minor>`        |
| `releasedir`   | Subdirectory in which a release is to be deployed                        | `branch/<release>-<date>` |
| `installdir`   | Root Installation directory                                              | `<datadir>/<releasedir>/` |
| `buildmode`    | Local build ('local') vs. via job submission  ('job')                    | local                     |
| `eb_options`   | String of options to pass "as is" to EasyBuild.                          |                           |
|                |                                                                          |                           |

Note that for each of the above variables, the corresponding environmental variable `$RESIF_<uppercase(variable)>` can be set.
Thus configuring RESIF can be done:

* using `resif` with command line arguments
* setting environment variables (`$RESIF_...`)
* providing one or more role configuration files

The order of preference for the different configuration types is as listed above, that is:

1. environment variables override the corresponding entries in the role configuration file
2. command line arguments in turn override the corresponding environment variables and matching entries in the role configuration file

In addition, as RESIF interacts with [Easybuild](https://hpcugent.github.io/easybuild), it sets several variables (prefixed with `eb_`) of interest for Easybuild that are listed below

| RESIF Variable   | Easybuild equivalent      | Description                                                                                | Default (if any)         |
|------------------|---------------------------|--------------------------------------------------------------------------------------------|--------------------------|
| `eb_prefix`      | `$EASYBUILD_PREFIX`       | Prefix directory for Easybuild installation                                                | `$HOME/.local/easybuild` |
| `eb_module_tool` | `$EASYBUILD_MODULES_TOOL` | Module tool, in [ 'Lmod', 'Tcl']                                                           |                          |
| `eb_buildpath`   | `$EASYBUILD_BUILDPATH`    | (temporary) directories to host builds -- you may want `/dev/shm` here                     | `<eb_prefix>/build`      |
| `eb_installpath` | `$EASYBUILD_INSTALLPATH`  | Root directory for installed software (`software/`) and modules (`modules/all/`) directory | `<eb_prefix>`            |


### `<user>`, `<group>`: Process owner/group

* all processes / jobs are run as this user `<user>` (__Default__: `$(whoami)`);
* all [sub]directory are assuming having read/write access for that user and/or group

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

### `<datadir>`: Specific Data directory

The data directory for RESIF (__Default__: `$HOME/.local/resif/`), setup by `resif init` -- see [`cli/index.md`](cli/index.md)).
It will typically hold the working copy(ies) of the Easybuild recipe repositories (_i.e._ [easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs) and [easyblocks](https://github.com/hpcugent/easybuild-easyblocks) used to install the software sets.

The typical layout of this directory is depicted below:

```bash
<datadir>
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


### `<buildmode>`: Build mode

The way the software package are built, _i.e._ either locally (`local`, __Default__) or via job submission on the platform (`job`). Default value:



### `<eb_options>`: Additional EB options

Use this variable to tweak the behavior of EasyBuild more in depth for options that are not supported directly by RESIF.
As an example to run the command as a "dry run":

~~~bash
$> resif build --eb-options "--dry-run" core
~~~

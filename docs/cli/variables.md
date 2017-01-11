-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 10:21 svarrette>

--------------------------
# RESIF Variables Overview

The workflow revolves around a few variables that are defined below.
Although it is interesting to take a look at them to personalize an installation, the script can be used without manually setting any of these options since the necessary ones have a default value.

Here are all the __RESIF__ variables that can be set, followed by their descriptions.

| RESIF Variable | Description                                                              | Default (if any)          |
|----------------|--------------------------------------------------------------------------|---------------------------|
| `user`         | User operating the process                                               | `<whoami>`                |
| `group`        | Group used for operating the process                                     |                           |
| `configdir`    | Configuration directory                                                  | `$HOME/.config/resif/`    |
| `datadir`      | Local Data directory                                                     | `$HOME/.local/resif/`     |
| `mns`          | Module Naming Scheme (see below)                                         | `categorized_mns`         |
| `release`      | Current release of the RESIF deployment (__differs__ from Resif version) | `v<major>.<minor>`        |
| `releasedir`   | Subdirectory in which a release is to be deployed                        | `<release>-<date>`        |
| `installdir`   | Root Installation directory                                              | `<datadir>/<releasedir>/` |

Note that for each of the above variables, the corresponding environmental variable `$RESIF_<uppercase(variable)>` can be set.

In addition, as RESIF interacts with [Easybuild](https://hpcugent.github.io/easybuild), it sets several variables (prefixed with `eb_`) of interest for Easybuild that are listed below

| RESIF Variable | Easybuild equivalent | Description                                 | Default (if any)         |
|----------------|----------------------|---------------------------------------------|--------------------------|
| `eb_prefix`    | `$EASYBUILD_PREFIX`  | Prefix directory for Easybuild installation | `$HOME/.local/easybuild` |
|                |                      |                                             |                          |

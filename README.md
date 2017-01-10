-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

[![By ULHPC](https://img.shields.io/badge/by-ULHPC-orange.svg)](http://hpc.uni.lu) [![Licence](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](http://www.gnu.org/licenses/gpl-3.0.html) [![gitlab](https://img.shields.io/badge/git-gitlab-lightgray.svg)](https://gitlab.uni.lu/ULHPC/resif) [![Issues](https://img.shields.io/badge/issues-gitlab-green.svg)](https://gitlab.uni.lu/ULHPC/resif/issues)

       Time-stamp: <Tue 2017-01-10 14:03 svarrette>

                           ____  _____ ____ ___ _____
                          |  _ \| ____/ ___|_ _|  ___|
                          | |_) |  _| \___ \| || |_
                          |  _ <| |___ ___) | ||  _|
                          |_| \_\_____|____/___|_|

       Copyright (c) 2015-2017 UL HPC Team <hpc-sysadmins@uni.lu>

# Revolutionary EasyBuild-based Software Installation Framework (RESIF)

RESIF is a wrapper on top of [Easybuild](https://hpcugent.github.io/easybuild) meant to pilot in an (hopefully) easy and reproducible way the building process of software used within the [UL HPC](http://hpc.uni.lu) platform.
This repository holds the __V2.0__ refactoring of the initial developments released on [Github](https://github.com/ULHPC/resif)

It comes with the following objectives in mind:

* Automatic Management of [Environment Modules](http://modules.sourceforge.net/) deployment
* Abstract version of Easybuild used
* Fully automates software builds and supports all available toolchains
* Clean (hierarchical) modules layout to facilitate its usage
* Easy to use
* Minimal requirements (Python 2.x, Ruby >= 1.9.3, Environment modules (Tcl/C or Lmod)
* Management of _software / module sets_ for which different policies applies, for instance:
  * `core`: set of software present by default, who deserve a special attention (automatic software testing reported on Cdash, etc.)
  * `ulhpc`: in addition to core, all **built** software availaible to the users
  * `biocore`: specific statck for Bio informaticians
* Coherent workflow for both the UL HPC sysadmins and users to cover the following scenarios:
  * [admin] Deployment from scratch of a new software stack
  * [user]  Build a new software on top of the existing stable stack
  * [power user]  as above, and contribute back to the deployed infrastructure (pull request etc.)
  * [admin] add a new software to a software set, on top of the existing stable stack
  * [admin] test the successful _building_ of a given software set (in `/tmp/` or `/dev/shm`)
  * [admin] prepare a new major / minor / patch release
* Reproducible and self-contained deployment, coupled with a strongly versioned release mechanism to facilitate access to old environments

For this purpose, the proposed workflow relies heavily on [Easybuild](http://hpcugent.github.io/easybuild/), a flexible framework for building/installing (scientific) software.

## Issues / Feature request

You can submit bug / issues / feature request using the [`ULHPC/resif` Project Tracker](https://gitlab.uni.lu/ULHPC/resif/issues)

## Licence

This project is released under the terms of the [GPL-3.0](LICENCE) licence.

[![Licence](https://www.gnu.org/graphics/gplv3-88x31.png)](http://www.gnu.org/licenses/gpl-3.0.html)

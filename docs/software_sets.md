-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 15:46 svarrette>

-----------------------------
# Software Sets aka Resiffile

Software sets are by default defined in `<configdir>/swsets/`.
Each of them comes as a YAML file which holds the list of software / module expected to be installed, what version to install, and where to fetch them from.

The format is depicted [__in `sample/swsets-format.yaml`__](sample/swsets-format.yaml).

## Global settings

The following settings can be used to control how the Resiffile installs and handles software.

### sources

Default [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) comes from the official EB Github repository, _i.e_:

* [easybuild-easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs)
* [easybuild-easyblocks](https://github.com/hpcugent/easybuild-easyblocks)

You might wish to configure for some of the software you wish to install your custom source for these repository, _i.e._

* your (private) fork of these repository holding your customized recipes
* your local copy of these repository your working on when developing your own recipes

You are free to give to each of these [custom] sources a short name you can refer to later when listing the eb files to build.

Expected format is as follows (see also `sample/swsets.yaml`)

~~~yaml
sources:
  "mysourceshortname":
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
Example:

~~~yaml
sources:
  "local":
    priority: 125
    easyconfigs:
      path: "$HOME/devel/easybuild/easyconfigs"
  "ulhpc_github":
    priority: 1
    easyconfigs:
      git: "https://github.com/ULHPC/easybuild-easyconfigs"
      branch: 'uni.lu'
    easyblocks:
      git: "https://github.com/ULHPC/easybuild-easyblocks"
~~~

In particular, the above setting means that when a given `<software>.eb` recipe is to be built, RESIF will search for it in the following order:

1. in the `<ulhpc_github>` source (priority:1)
2. the default source (priority: 50)
3. the `local` source (priority: 75)

It means the following layout for RESIF `<datadir>` (_i.e._ `~/.local/resif` by default, see [variables.md](variables.md)):

```bash
<datadir>
├── easyblocks
│   ├── default/      # default easyblocks sources i.e. git from hpcugent/easybuild-easyblocks
│   │   ├── CONTRIBUTING.md
│   │   └── [...]
│   ├── ulhpc_github/ # custom easyblocks sources  from ULHPC/easybuild-easyblocks fork
│   │   ├── CONTRIBUTING.md
│   │   └── [...]
│   └── local -> /path/to/local/easyblocks  # Local symlink to the path
└── easyconfigs     # default easyconfig sources i.e. git from hpcugent/easybuild-easyblocks
    ├── default
    │   ├── CONTRIBUTING.md
    │   └── [...]
    ├── ulhpc_github/
    │   ├── CONTRIBUTING.md
    │   └── [...]
    └── local -> /path/to/local/easyconfigs
```

_Note_: you might want to define __permanently__ these custom sources in `<configdir>/swsets/<mysourceshortname>.yaml` to avoid having to repeat this information in your software sets


### toolchains

To build software with EasyBuild, the first thing you'll need to do is either pick a supported compiler toolchain, or construct your own and make EasyBuild support it.
A _toolchain_ is a collection of tools to build (HPC) software consistently.
It consists of:

* compilers for C/C++ and Fortran,
* a communications library (MPI), and
* mathematical libraries (linear algebra, FFT).

On your site, you typically wish to restrict to a few of the [supported compiler toolchains](http://easybuild.readthedocs.io/en/latest/eb_list_toolchains.html) (obtained by `eb --list-toolchains`).

You can use the global `toolchains:` directive to list the ones you wish to consider, typically as follows:

```yaml
###############################
# Default Toolchains to Build #
###############################
# get the list of  supported compiler toolchains using:
#      eb --list-toolchains
# See also http://easybuild.readthedocs.io/en/latest/eb_list_toolchains.html
toolchains:
- foss
- intel
- gmvolf
```

Most interesting toolchains:

| Toolchain | Description                     | Compilers      | MPI stack | Included Libraries                       |
|-----------|---------------------------------|----------------|-----------|------------------------------------------|
| `foss`    | Free & Open Source Software     | GCC            | OpenMPI   | OpenBLAS/LAPACK, ScaLAPACK(/BLACS), FFTW |
| `intel`   | Intel-based software            | `icc`, `ifort` | `impi`    | `imkl`                                   |

In addition, you might consider the following ones:

| Toolchain | Description                     | Compilers      | MPI stack | Included Libraries                       |
|-----------|---------------------------------|----------------|-----------|------------------------------------------|
| `gmvolf`  | Open Source with MVAPICH2       | GCC            | MVAPICH2  | OpenBLAS/LAPACK, ScaLAPACK(/BLACS), FFTW |
| `cgmvolf` | Clang Open Source with MVAPICH2 | Clang/GCC      | MVAPICH2  | OpenBLAS/LAPACK, ScaLAPACK(/BLACS), FFTW |
| `cgoolf`  | Clang Open Source               | Clang/GCC      | OpenMPI   | OpenBLAS/LAPACK, ScaLAPACK(/BLACS), FFTW |

When building your software sets, each software listed will be build for each listed toolchains __if possible__

### default software set

Comes under `default:` according to the software set definition below.
It holds the set of software to be present by default, which deserve a special attention (automatic software testing reported on Cdash, etc.)

## Software Set

```yaml
<name>:
- <software1>.eb [: <sourcename>]
- <software2>.eb [: <sourcename>]
- ...
```

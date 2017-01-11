-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 16:31 svarrette>

-----------------------------
# Software Sets aka Resiffile

Software sets are by default defined in `<configdir>/swsets/`.
Each of them comes as a YAML file which holds the list of software / module expected to be installed, what version to install, and where to fetch them from.

The format is depicted [__in `sample/swsets-format.yaml`__](sample/swsets-format.yaml).

## Global settings

The following settings can be used to control how the Resiffile installs and handles software.

### sources

See [`ebsources.md`](ebsources.md)

Default [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) comes from the official EB Github repository, _i.e_:

* [easybuild-easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs)
* [easybuild-easyblocks](https://github.com/hpcugent/easybuild-easyblocks)

You might wish to configure for some of the software you wish to install your custom source for these repository
Expected format is as follows (see also `sample/swsets.yaml`)

~~~yaml
sources:
  "mysourceshortname":
    [...] use here the same format as for ebsources.md
~~~
Example:

~~~yaml
sources:
  "local":
    priority: 75
    easyconfigs:
      path: "$HOME/devel/easybuild/easyconfigs"
~~~

It means the following layout for RESIF `<datadir>` (_i.e._ `~/.local/resif` by default, see [variables.md](variables.md)):

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
    ├── default
    │   ├── CONTRIBUTING.md
    │   └── [...]
    ├── ulhpc_github/
    │   ├── CONTRIBUTING.md
    │   └── [...]
    └── local -> /path/to/local/easyconfigs
```

_Note_: you might want to define __permanently__ these custom sources in `<configdir>/swsets/<mysourceshortname>.yaml` to avoid having to repeat this information in your software sets, as described [here](ebsources.md)


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
- foss/2016a
- foss/2016b
- intel/2016a
- intel/2016b
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

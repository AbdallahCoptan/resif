-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Thu 2017-01-12 15:14 svarrette>

-----------------------------
# Software Sets aka. RESIFile

Software sets are by default defined in `<configdir>/swsets/` but you can of course provide your own from any location and pass it as parameter to `resif`.
Each RESIFile comes as a YAML file which holds the list of software / module expected to be installed, what version to install, and where to fetch them from.

The format is depicted [__in `sample/swsets-format.yaml`__](sample/swsets-format.yaml).

## Global settings

The following settings can be used to control how the RESIFile installs and handles software.

### sources (optional)

You might want to precise here one or multiple custom sources for [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) that you **haven't** configured in `<configdir>/sources/<shortname>.yaml` (for instance if you want to use this source only once for the considered software set), as follows (see also `sample/swsets.yaml` and [`ebsources.md`](ebsources.md)):

~~~yaml
sources:
  "mysourceshortname":
    [...] use here the same format as for ebsources.md
~~~

Example:

~~~yaml
sources:
  "local-devel":
    priority: 75
    easyconfigs:
      path: "$HOME/devel/easybuild/easyconfigs"
~~~

_Note_: you might want to define __permanently__ these custom sources in `<configdir>/swsets/<mysourceshortname>.yaml` to avoid having to repeat this information in your software sets, as described [here](ebsources.md).

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
- gmvolf/2016a
```

__Note__: You precise the name of the compiler toolchains in the form `<toolchain>/<version>`.

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

Comes under `default:` as a list of software specifications according to the below format.
It holds the set of software to be present by default (in addition ), which deserve a special attention (automatic software testing reported on Cdash, etc.)

## Software Specifications

You can refer to a given software to install (according to a Easybuild recipe) according to one for the following forms:

~~~bash
- <softname>-<version>-<toolchain>.eb   # Ex: HPL-2.1-foss-2016.06.eb, means install exactly that EB file
- <softname>/<version>                  # Ex: HPL/2.1, means search for HPL-2.1*.eb and build the latest for the considered toolchains
- <softname>/<version>-<versionsuffix>
~~~

## Software Set

A software set is simply a **list** of software specifications under a named namespace `<name>`, _i.e._ as follows:

```yaml
<name>:
- <software1>.eb
- <software2>.eb
- ...
```

For instance, the below example defines **two** software sets (named `default` and `lcsb`).
Recall that you **SHOULD** have a default software set
Ex:

```yaml
default:   # Default software set
- HPL/2.1
- HPCG-2.1-goolf-1.4.10.eb
lcsb:
- STAR-2.5.1b-ictce-7.3.5.eb
```

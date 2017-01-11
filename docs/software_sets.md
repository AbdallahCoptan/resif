-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 11:57 svarrette>

-----------------------------
# Software Sets aka Resiffile

Software sets are by default defined in `<configdir>/swsets/`.
Each of them comes as a YAML file which holds the list of software / module expected to be installed, what version to install, and where to fetch them from.

The format of is as follows:

~~~yaml
# Optional definition of custom sources for Easybuild recipes i.e. easy{configs,blocks}
# if they differ from the default ones
sources:
~~~

See also `sample/swsets.yaml`

## Global settings

The following settings can be used to control how the Resiffile installs and handles software.

### sources

Default [Easybuild](https://hpcugent.github.io/easybuild) recipes (_i.e._ easyconfigs and easyblocks) comes from the official EB Github repository, _i.e_:

* [easybuild-easyconfigs](https://github.com/hpcugent/easybuild-easyconfigs)
* [easybuild-easyblocks](https://github.com/hpcugent/easybuild-easyblocks)

You might wish to configure for some of the software you wish to install your custom source for these repository, _i.e._

* your (private) fork of these repository holding your customized recipes
* your local copy of these repository your working on when developing your own recipes

Sources

### toolchains

To build software with EasyBuild, the first thing you'll need to do is either pick a supported compiler toolchain, or construct your own and make EasyBuild support it.
On your site, you typically wish to restrict to a few of the supported compiler toolchains (obtained by `eb --list-toolchains`)

You can use the global `:toolchains` directive to list the ones you wish to consider when building your software set such that each software listed will

### default software set

Comes under `default:` according to the software set definition below
It holds the set of software to be present by default, which deserve a special attention (automatic software testing reported on Cdash, etc.)

## Software Set

```yaml
<name>:
  - <software1>.eb [: <sourcename>]
  - <software2>.eb [: <sourcename>]
  - ...
```


core: set of software present by default, which deserve a special attention (automatic software testing reported on Cdash, etc.)
ulhpc: in addition to core, all built software availaible to the users of the UL HPC platform.
In practice, each software set is assigned a dedicated section of the YAML configuration file software_sets.yaml precising the software it holds, for instance:

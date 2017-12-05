-------------------------------
# RESIF Command Line Interface (CLI)

| Command                      | Description                                                                         |
|------------------------------|-------------------------------------------------------------------------------------|
| `init`                       | Initialize RESIF on your machine                                                    |
| `new`                        | Create a new recipe / software sets definition                                      |
| `build`                      | Build and deploy the configured software sets.                                      |
| `release`                    | Release a new version of the defined software sets                                  |                                                  |
| `sources {add,info,list,rm}` | List/Add/Remove configured EB-[configs,blocks] sources                              |
| `list`                       | List all available software sets                                                    |
| `info`                       | Display detailed information about a software set                                   |
| `version`                    | Prints Resif's version information                                                  |
| `bump`                       | Bump the _general_ release of the RESIF deployment (__differs__ from Resif version) |
| `export`                     | Export the deployement configuration for further reproducible builds                |
| `import`                     | Import a deployment configuration 

These commands relies on a set of [internal variables](../variables.md) to perform each action.

## resif init

This command initializes / sets up a working RESIF environment.
In practice, it performs the following actions:

1. initialize `<configdir>` (in `~/.config/resif` by default), typically as a clone of a `resif-control` repository.
   Otherwise, it initializes `<configdir>` as follows:
    - prepare default software sets `<configdir>/swsets/default.yaml`
    - prepare the default role (specializing the [RESIF variables](../variables.md))     `<configdir>/roles/default.yaml`
    - bootstrap the deployment version (used as `<release>`) if needed `<configdir>/VERSION`
    - prepare the default EB source definition `<configdir>/sources/default.yaml`, which holds configuration for the Easybuild repository sources -- see [`ebsources.md`](../ebsources.md)
2. initialize `<datadir>`  (`~/.local/resif` by default)
    - create directories for `devel` and `production` deployment
    - setup the EB source repository (according to the definitions found in `<configdir>/sources/*.yaml`), _i.e._:
    
         * `<datadir>/easyconfigs/<sourcename>/`, a clone of the [easybuild-easyconfigs repository](https://github.com/hpcugent/easybuild-easyconfigs) which hosts EasyBuild specification files for the source `<sourcename>`
         * `<datadir>/easyblocks/<sourcename>/`, a clone of the [easybuild-easyblocks repository](https://github.com/hpcugent/easybuild-easyblocks) which hosts implementations of install procedures

3. install [Easybuild](https://hpcugent.github.io/easybuild) according to the official [bootstrapping procedure](http://easybuild.readthedocs.io/en/latest/Installation.html#bootstrapping-easybuild) in `EASYBUILD_PREFIX=$HOME/.local/easybuild`
4. (asks you to) export a set of environment variables:
     - `$RESIF_CONFIGDIR`
     - `$EASYBUILD_PREFIX`
     - `$EASYBUILD_MODULES_TOOL` (to 'Lmod')


## resif build

This command builds a software set to `<datadir>/devel` according to:

* either the path to a [`RESIFile`](../RESIFile.md) defining the software sets we wish to build and the configuration to use
* or the name `<name>` of one of the pre-defined software sets under `<configdir>/swsets/<name>.yaml` -- see [`variables.md`](../variables.md)

Then, this command performs the following tasks:

1. (eventually) define new [EB sources](../ebsources.md) to be used to get the EasyBuild recipes
2. pull all EB sources defined under `<datadir>/easy{blocks,configs}/*/` to get the up-to-date commits of these sources
3. for each software set `<swset>`:
4. for each sofware `<software>`
    * if defined as `<software>-<version>-<toolchain>.eb`: build it using `eb --robot [...]` under `<installdir>/<swset>/`
    * else if defined as `<software>/<version>`:
         - for each toolchain `<toolchain>`, find the appropriate [list of] `*.eb` source matching these constraints
               * if found, install them
               * (optional) else, try to find a `*.eb` file where the toolchain is from the same year as the expected one and [try to] build it using `eb --robot --try-toolchain=<toolchain>,<toolchainversion> [...]`

## resif release

This command does the same as `resif build`, but the `<installdir>` is `<datadir>/production/v<versionmajor>.<versionminor>-<date>`. 

## resif export

__TODO__: define what it should do and implement it

## resif import

__TODO__: define what it should do and implement it
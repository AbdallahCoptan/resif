-------------------------------
# RESIF Command Line Interface (CLI)

| Command                 | Description                                                          |
|-------------------------|----------------------------------------------------------------------|
| `init`                  | Initialize RESIF on your machine                                     |
| `new`                   | Create a new recipe / software sets definition                       |
| `build`                 | Build and deploy the configured software sets.                       |
| `release`               | Release a new version of the defined software sets                   |
| `export`                | Export the deployement configuration for further reproducible builds |
| `import`                | Import a deployment configuration                                    |
| `sources {add,list,rm}` | List/Add/Remove configured EB-[configs,blocks] sources               |
| `list`                  | List all available software sets                                     |
| `info`                  | Display detailed information about a software set                    |
| `version`               | Prints Resif's version information                                   |

These commands relies on a set of [internal variables](../variables.md) to perform each action.

## resif init

This command initialize / setup a working RESIF environment.
In practice, it performs the following actions:

1. initialize `<configdir>` (`~/.config/resif` by default)
    - prepare default software sets `<configdir>/swsets/default.yaml`
    - prepare the default roles (each of them specializing the [RESIF variables](../variables.md))     `<configdir>/roles/{default,sysadmin}.yaml`
    - bootstrap the deployment version (used as `<release>`) if needed `<configdir>/VERSION`
    - prepare the default EB source definition `<configdir>/sources/default.yaml`, which holds configuration for the Easybuild repository sources -- see [`ebsources.md`](../ebsources.md)
2. initialize `<datadir>`   (`~/.local/resif`  by default)
    - setup the EB source repository (according to the definitions found in `<configdir>/sources/*.yaml`), _i.e._:
          * `<datadir>/easyconfigs/<sourcename>/`, a clone of the [easybuild-easyconfigs repository](https://github.com/hpcugent/easybuild-easyconfigs) which hosts EasyBuild specification files for the source `<sourcename>`
          * `<datadir>/easyblocks/<sourcename>/`, a clone of the [easybuild-easyblocks repository](https://github.com/hpcugent/easybuild-easyblocks) which hosts implementations of install procedures

3. install [Easybuild](https://hpcugent.github.io/easybuild) according to the official [bootstrapping procedure](http://easybuild.readthedocs.io/en/latest/Installation.html#bootstrapping-easybuild) in `EASYBUILD_PREFIX=$HOME/.local/easybuild`
4. creates `<installdir>`
5. (ask to ) export a set of Environment variables:
     - `$EASYBUILD_PREFIX`
     - `$EASYBUILD_MODULES_TOOL` (to 'Lmod')


## resif build

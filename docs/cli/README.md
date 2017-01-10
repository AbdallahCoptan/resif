-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Tue 2017-01-10 22:54 svarrette>

-------------------------------
# RESIF Command Line Interface (CLI)

**Prerequisites:**

To install this script, you need to have some required packages installed on your computer:

- python 2.6 or above __TODO__ rework version
- `git`
- `pip` to install and uninstall the script (On Ubuntu, simply install the `python-pip` package.)
-  Environment module (or Lmod) set on your system.

See the other pages of this documentation for [more details about these tools](https://gitlab.uni.lu/modules/infrastructure/wikis/overview) and the [installation instructions for Lmod](appendix/Lmod-install.md).

### Main commands Overview

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

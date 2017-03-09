-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 10:20 svarrette>
-------------------
# [Lmod](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod)

[Lmod](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod)  is a [Lua](http://www.lua.org/) based module system that easily handles the `MODULEPATH` Hierarchical problem.

Lmod is a new implementation of Environment Modules that easily handles the MODULEPATH Hierarchical problem. It is drop-in replacement for TCL/C modules and reads TCL modulefiles directly.
In particular, Lmod add many interesting features on top of the traditional implementation focusing on an easier interaction (search, load etc.) for the users.

* [User guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/user-guide)
* [Advanced user guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/advanced-user-guide)
* [Sysadmins Guide](https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/system-administrators-guide)

## Under Mac OS X

The best is to use [HomeBrew](http://brew.sh)

~~~bash
$> brew install lua
# Homebrew does not provide special Lua dependencies
$> luarocks-5.2 install luafilesystem   
$> luarocks-5.2 install luaposi
~~~

_Note_:  You can also use `--local` option (or the `--tree <path>`) to have the LUA packages installed in `~/.luarocks` (or `<path>`). If you use `--tree <path>`, you need to update the environmental variables [`LUA_PATH` and `LUA_CPATH`](http://leafo.net/guides/customizing-the-luarocks-tree.html) as follows:

~~~bash
export LUA_PREFIX="$HOME/.local/share/luarocks"
export LUA_PATH="$LUA_PREFIX/share/lua/5.2/?.lua;$LUA_PATH"
export LUA_CPATH="$LUA_PREFIX/lib/lua/5.2/?.so;$LUA_CPATH"
~~~

Now it should be fine to install LMod:

~~~bash
$> brew install lmod
~~~

After this installation:

* `lmod` command is located in `$(brew --prefix lmod)/libexec` and you probably wants to make an **alias** for it

          alias lmod='$(brew --prefix lmod)/libexec/lmod'

* You may want to load LMOD variables from your favorite shell init script:

          source $(brew --prefix lmod)/init/$(basename $SHELL)

## Under Linux/CentOS

**Prerequisites:** You need to have the EPEL testing repositories in the sources list. (Do not enable it by default). Then install the Lmod package using this repo.

~~~bash
$> yum install epel-release -y
$> yum install --enable-repo=epel-testing Lmod
~~~

You can now use Lmod in a version compatible with EasyBuild.

## Under Ubuntu/Debian

__TODO__ those are the old notes of Maxime, probably outdated.

**Prerequisites:** You need to have the sid repository in your sources list (the lmod package from jessie is too old and therefore not compatible with EasyBuild). And we are going to make sure that this repo is not going to be used for anything else except if we specify it directly.

1. Add the sid repository to your sources list:
    * Create a file named `debian-sid.list` in `/etc/apt/sources.list.d`
    *  Write the following content inside it:

            # sid repository - main, contrib and non-free branches
            deb http://http.us.debian.org/debian sid main non-free contrib
            deb-src http://http.us.debian.org/debian sid main non-free contrib

2. Set your default Debian release. Create or modify `/etc/apt/apt.conf.d/99defaultrelease` to match the following content:

         APT::Default-Release "wheezy"

    Eventually replacing _wheezy_ with the name of your release if different.


Now you can install the `lmod` package using this repository:

~~~bash
$> apt-get update
$> apt-get install -y -t sid lmod
~~~

You can now use Lmod in a version compatible with EasyBuild.

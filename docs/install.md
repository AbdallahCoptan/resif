-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Wed 2017-01-11 10:25 svarrette>

-------------------
# Requirements

The only strict requirements are:

* Linux or Mac OS X
* Python version 2.6, or a more recent 2.x version + `setuptools`, `vsc-install` & `vsc-base`
     - see also [Required Python packages of Easybuild](http://easybuild.readthedocs.io/en/latest/Installation.html#required-python-packages)
* a working `git`
* `pip` to install and uninstall the script (On Ubuntu, simply install the `python-pip` package.)
* a __modules tool__: _i.e._ Tcl(/C) environment modules or (better) [Lmod](http://lmod.sourceforge.net).
  Currently supported module tools:
     - __(recommended)__ [Lmod](http://lmod.sourceforge.net/) (version >= 5.6.3)
     - [Tcl/C environment-modules](http://modules.sourceforge.net/) (version >= 3.2.10)
     - [Tcl-only variant of environment modules](http://sourceforge.net/p/modules/modules-tcl)

**Under Mac OS**:

the actual module command/script (modulecmd, modulecmd.tcl or lmod) must be available via $PATH
see Required modules tool for more details
For more information on (optional) dependencies, see Dependencies.

## Installation from git

#### With root permissions

Clone the git repository:

    git clone https://gitlab.uni.lu/ULHPC/resif.git

Then go to in this directory and type the following command to install the script:

    python setup.py sdist && pip install dist/*

#### Without root permissions

Clone the git repository:

    git clone https://gitlab.uni.lu/ULHPC/resif.git

Then go to in this directory directory and type the following command to install the script:

    python setup.py sdist && pip install --install-option="--prefix=$HOME/.local" dist/*
Note that you can replace `$HOME/local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/.local/bin` to you path:

    export PATH=$PATH:$HOME/.local/bin
and `$HOME/.local/lib/python2.7/site-packages` to your pythonpath:

    export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.


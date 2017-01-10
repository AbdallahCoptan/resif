-*- mode: markdown; mode: visual-line; fill-column: 80 -*-

        Time-stamp: <Tue 2017-01-10 23:01 svarrette>

-------------------
## Install from PyPi (recommended)

#### With root permissions

Simply use the following command:

    pip install resif

You can now start using the command, see below for more information.

#### Without root permissions

Use the following command to install the command:

    pip install --install-option="--prefix=$HOME/.local" resif

Note that you can replace `$HOME/.local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/.local/bin` to you path to make the command accessible:

    export PATH=$PATH:$HOME/.local/bin
and `$HOME/.local/lib/python2.7/site-packages` to your pythonpath so that the command's dependencies are accessible:

    export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.

## Installation from git

#### With root permissions

Clone the git repository:

    git clone https://github.com/ULHPC/resif.git

Then go to in this directory and type the following command to install the script:

    python setup.py sdist && pip install dist/*

#### Without root permissions

Clone the git repository:

    git clone https://github.com/ULHPC/resif.git

Then go to in this directory directory and type the following command to install the script:

    python setup.py sdist && pip install --install-option="--prefix=$HOME/.local" dist/*
Note that you can replace `$HOME/local` by anything you want as long as you have all the right for this location, just modify the following commands accordingly.

Add then `$HOME/.local/bin` to you path:

    export PATH=$PATH:$HOME/.local/bin
and `$HOME/.local/lib/python2.7/site-packages` to your pythonpath:

    export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
Note that in this last path, the part `python2.7` may change depending on the python version you use on your computer. Just modify the previous path accordingly to what is actually present in your tree at this point.

The Module Naming Scheme (MNS) affect the way the modules (resp. the software packages) are organized behind the `<moduledir>` directory.
In particular, software modules are installed in their own subdirectory following the active [module naming scheme](http://easybuild.readthedocs.io/en/latest/api/easybuild.tools.module_naming_scheme.html), which can be one of the following:

| Naming Scheme       | Software package/Modulefiles subdirectory layout             | Example                          |
|---------------------|--------------------------------------------------------------|----------------------------------|
| `categorized_mns`   | `<moduleclass>/<name>/<version>-<toolchain><versionsuffix>`  | biology/ABySS/1.3.4-goolf-1.4.10 |
| `categorized_hmns`  | `<moduleclass>/<toolchain>/<versionsuffix>/<name>/<version>` | MPI/GCC/4.8.3/OpenMPI/1.6.5      |
| `easybuild_mns`     | `<name>/<version>-<toolchain><versionsuffix>`                | OpenFOAM/2.1.1-goolf-1.4.10      |
| `hierarchical_mns`  | `<moduleclass>/<toolchain>-<versionsuffix>/<name>/<version>` | Bio/ictce-5.3.0/ABySS/1.3.4      |

By default, RESIF promotes the [Categorized MNS](http://easybuild.readthedocs.io/en/latest/api/easybuild.tools.module_naming_scheme.categorized_mns.html).
In particular, upon building of a software set, the typical layout obtained for the modules would look like that:

~~~bash
<moduledir>
  ├── all           # Reference for **all** modules
  │   ├── base/
  │   ├── bio/
  │   ├── cae/
  │   ├── chem/
  │   ├── compiler/
  │   ├── data/
  │   ├── debugger/
  │   ├── devel/
  │   ├── lang/
  │   ├── lib/
  │   ├── math/
  │   ├── mpi/
  │   ├── numlib/
  │   ├── phys/
  │   ├── system/
  │   ├── toolchain/
  │   ├── tools/
  │   └── vis/
  ├──  base         # permits to eventually have MODULEPATH focusing on the 'base' category
  │   └── base
  │       ├── EasyBuild
  │       └── MATLAB
  │           ├── 2016a -> <moduledir>/all/base/MATLAB/2016a    # Symlink to modulefile on 'all'
  │           └── 2016b -> <moduledir>/all/base/MATLAB/2016a
  ├──  bio         # permits to eventually have MODULEPATH focusing on the 'bio' category
  │   └── bio
  │       ├──  ABySS
  │       │   └── 1.5.2-goolf-1.4.10 -> <moduledir>/all/bio/ABySS/1.5.2-goolf-1.4.10
  [...]
~~~

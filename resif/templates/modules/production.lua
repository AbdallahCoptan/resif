help([[

Description
===========
Set up UL HPC software environment: {{ buildtype }} version {{ versionstamp }} .

More information
================
 - Homepage: http://hpc.uni.lu
]])

whatis([[Description: Set up UL HPC software environment for {{ buildtype }} version {{ versionstamp }} ]])
whatis([[Homepage: http://hpc.uni.lu]])

local root = "{{ path }}"

conflict("swset")

prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))

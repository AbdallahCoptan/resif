help([[

Description
===========
Set up UL HPC development software environment for {{ buildtype }} version {{ versionstamp }}.

More information
================
 - Homepage: http://hpc.uni.lu
]])

whatis([[Description: Set up UL HPC development software environment for {{ buildtype }} version {{ versionstamp }}.]])
whatis([[Homepage: http://hpc.uni.lu]])

local root = "{{ path }}"

conflict("swset")

if mode() == "load" then
    io.stderr:write([==[Module warning: The development software environment is not guaranteed to be stable!
]==])
end

prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))

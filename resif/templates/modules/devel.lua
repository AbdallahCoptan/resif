help([[

Description
===========
Set up UL HPC development software environment for {{ swset }} {{ buildtype }}, version {{ versionstamp }}.

More information
================
 - Homepage: http://hpc.uni.lu
]])

whatis([[Description: Set up UL HPC development software environment for {{ swset }} {{ buildtype }}, version {{ versionstamp }}.]])
whatis([[Homepage: http://hpc.uni.lu]])

local root = "{{ path }}"
local controlled = os.getenv("SWENV_CONTROLLED") or "false"

-- conflict("swset")

if mode() == "load" then
    io.stderr:write([==[Module warning: The development software environment is not guaranteed to be stable!
]==])
end

setenv("SWENV_CONTROLLED", "true")

if controlled == "true" then
  prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))
else
  setenv("MODULEPATH", "{{ modulerootpath }}/../")
  prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))
end


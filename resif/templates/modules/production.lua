help([[

Description
===========
Set up UL HPC software environment: {{ swset }} {{ buildtype }}, version {{ versionstamp }}.

More information
================
 - Homepage: http://hpc.uni.lu
]])

whatis([[Description: Set up UL HPC software environment for {{ swset}} {{ buildtype }}, version {{ versionstamp }} ]])
whatis([[Homepage: http://hpc.uni.lu]])

local root = "{{ path }}"
local controlled = os.getenv("SWENV_CONTROLLED") or "false"

-- conflict("swset")

family("{{ swset }}")

setenv("SWENV_CONTROLLED", "true")

if controlled == "true" then
  prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))
else
  pushenv("MODULEPATH", "{{ modulerootpath }}/../")
  prepend_path("MODULEPATH", pathJoin(root, "modules", "all"))
end


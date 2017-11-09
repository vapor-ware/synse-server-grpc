# Packaging for Python

# this currently goes on the assumption that python 2 is run via the `python`
# binary, and python3 is run by the `python3` binary. this is not the best way
# of doing this, but it is a start.
HAS_PY2 := $(shell command -v python)
HAS_PY3 := $(shell command -v python3)


pip-package:  ## Package the python package into a tarball
	cd python ; python setup.py sdist


pip-install:  ## Install the python package from tarball
ifdef HAS_PY2
	cd python ; pip install dist/synse_plugin-*.tar.gz
endif
ifdef HAS_PY3
	cd python ; pip3 install dist/synse_plugin-*.tar.gz
endif


pip-einstall:  ## Install the python package in editable mode
ifdef HAS_PY2
	pip install -I -e ./python
endif
ifdef HAS_PY3
	pip3 install -I -e ./python
endif


pip-uninstall:  ## Uninstall the synse_plugin package via pip
ifdef HAS_PY2
	cd python ; pip uninstall -y synse_plugin
endif
ifdef HAS_PY3
	cd python ; pip3 uninstall -y synse_plugin
endif


pip-clean:  ## Remove the python packaging build artifacts
	cd python ; rm -rf build dist synse_plugin.egg-info


.PHONY: pip-package pip-install pip-einstall pip-uninstall pip-clean
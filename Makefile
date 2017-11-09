
# Make GRPC client/server source files for the target languages
# -------------------------------------------------------------

python:  ## Build the GRPC source for Python
	docker run \
	    -v `pwd`:/build \
	    grpc/python:1.4 \
	    python3 -m grpc_tools.protoc -I/build \
	        --python_out=/build/python/synse_plugin \
	        --grpc_python_out=/build/python/synse_plugin \
	        /build/synse.proto && \
	sed -i -e 's/import synse_pb2 as synse__pb2/from . import synse_pb2 as synse__pb2/g' python/synse_plugin/synse_pb2_grpc.py && \
	if [ -f "python/synse_plugin/synse_pb2_grpc.py-e" ]; then rm python/synse_plugin/synse_pb2_grpc.py-e; fi;



go:  ## Build the GRPC source for Go
	docker run \
	    -v `pwd`:/build \
	    grpc/go:1.0 \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build/go


all: python go  ## Build source for all supported languages



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


help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


.PHONY: all go help python pip-package pip-install pip-einstall pip-uninstall pip-clean
.DEFAULT_GOAL := help
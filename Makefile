
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


help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


pip-package:
	cd python ; python setup.py sdist

pip-install:
	@# this could also be done from here with pip install -I -e ./python -- this  makes it editable..
	cd python ; pip install dist/synse_plugin-*.tar.gz

pip-uninstall:
	cd python ; pip uninstall -y synse_plugin

pip-clean:
	cd python ; rm -rf build dist synse_plugin.egg-info


.PHONY: all go help python
.DEFAULT_GOAL := help
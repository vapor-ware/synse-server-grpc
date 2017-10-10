
# Make GRPC client/server source files for the target languages
# -------------------------------------------------------------

python:  ## Build the GRPC source for Python
	docker run \
	    -v `pwd`:/build \
	    grpc/python:1.4 \
	    python -m grpc_tools.protoc -I/build --python_out=/build/python --grpc_python_out=/build/python /build/synse.proto


go:  ## Build the GRPC source for Go
	docker run \
	    -v `pwd`:/build \
	    grpc/go:1.0 \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build/go


all: python go  ## Build source for all supported languages


help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


.PHONY: all go help python
.DEFAULT_GOAL := help
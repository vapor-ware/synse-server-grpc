#
# Synse Server gRPC
#

PKG_NAME := synse_grpc
PKG_VER  := $(shell python python/version.py)

.PHONY: python
python:  ## Build the GRPC source for Python
	@printf "Generating Python source."
	@docker run \
	    -v `pwd`:/build \
	    grpc/python:1.4 \
	    python3 -m grpc_tools.protoc -I/build \
	        --python_out=/build/python/synse_grpc \
	        --grpc_python_out=/build/python/synse_grpc \
	        /build/synse.proto && \
	sed -i -e 's/import synse_pb2 as synse__pb2/from . import synse_pb2 as synse__pb2/g' python/synse_grpc/synse_pb2_grpc.py && \
	if [ -f "python/synse_grpc/synse_pb2_grpc.py-e" ]; then rm python/synse_grpc/synse_pb2_grpc.py-e; fi;
	@printf " [done]\n"

.PHONY: go
go:  ## Build the GRPC source for Go
	@printf "Generating Go source."
	@docker run \
	    -v `pwd`:/build \
	    grpc/go:latest \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build/go
	@printf " [done]\n"

.PHONY: all
all: python go  ## Build source for all supported languages

.PHONY: github-tag
github-tag:  ## Create and push a tag with the current version
	git tag -a ${PKG_VERSION} -m "${PKG_NAME} version ${PKG_VERSION}"
	git push -u origin ${PKG_VERSION}

.PHONY: py-publish
py-publish: ## Build and publish the python package to PyPi
	pip install 'twine>=1.5.0'
	cd python ; python setup.py sdist bdist_wheel --universal
	cd python ; twine upload dist/*
	cd python ; rm -rf build dist .egg synse_grpc.egg-info

.PHONY: version
version:  ## Print the current version of Synse Server gRPC
	@echo "$(PKG_VER)"

.PHONY: help
help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help

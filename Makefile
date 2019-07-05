#
# Synse Server gRPC
#

PKG_NAME := synse_grpc
# FIXME: python setuptools is apparently not complaint with SemVer:
#   .../python3.6/site-packages/setuptools/dist.py:472: UserWarning: Normalizing '3.0.0-alpha.1' to '3.0.0a1'
#      normalized_version,
#      3.0.0a1
# https://github.com/pypa/setuptools/issues/308
#
# Since we build our tags off of this version, we can't get the version via the commented
# out line below - instead, we'll just awk it from the file directly. Its fine if the
# version on pypi is normalized for now.
#PKG_VER  := $(shell python python/setup.py --version)
PKG_VER := $(shell (cd python/ && python -c "import synse_grpc ; print(synse_grpc.__version__)"))

.PHONY: python
python:  ## Build the gRPC source for Python
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
go:  ## Build the gRPC source for Go
	@printf "Generating Go source."
	@docker run \
	    -v `pwd`:/build \
	    grpc/go:latest \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build/go
	@printf "     [done]\n"

.PHONY: all
all: python go  ## Build source for all supported languages

.PHONY: github-tag
github-tag:  ## Create and push a tag with the current version
	git tag -a ${PKG_VER} -m "${PKG_NAME} version ${PKG_VER}"
	git push -u origin ${PKG_VER}

.PHONY: version
version:  ## Print the current version of Synse gRPC
	@echo "${PKG_VER}"

.PHONY: help
help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help

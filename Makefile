#
# Synse Server gRPC
#

PKG_NAME := $(shell python python/setup.py --name)
PKG_VER  := $(shell python python/setup.py --version)

.PHONY: python
python:  ## Build the gRPC source for Python
	@printf "Generating Python source."
	@docker run \
		-v `pwd`:/defs \
		namely/protoc-all \
		-f synse.proto \
		-o python/synse_grpc/ \
		-l python
	rm python/__init__.py
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

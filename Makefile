
# Make GRPC client/server source files for the target languages
# -------------------------------------------------------------

# Make targets are organized by functionality in the 'make' subdirectory
include make/build.make
include make/github.make
include make/pip.make

PKG_VER := $(shell python python/version.py)


version:  ## Print the current version of Synse Server gRPC
	@echo "$(PKG_VER)"

help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort


.PHONY: help version
.DEFAULT_GOAL := help
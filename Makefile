#
# Synse Server gRPC
#

# Make targets are organized by functionality in the 'make' subdirectory
include make/build.make
include make/github.make

PKG_VER := $(shell python python/version.py)


.PHONY: py-publish
py-publish: ## Build and publish the python package to PyPi
	pip install 'twine>=1.5.0'
	cd python ; python setup.py sdist bdist_wheel --universal
	cd python ; twine upload dist/*
	cd python ; rm -rf build dist .egg synse_plugin.egg-info

.PHONY: version
version:  ## Print the current version of Synse Server gRPC
	@echo "$(PKG_VER)"

.PHONY: help
help:  ## Print usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help

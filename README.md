[![CircleCI](https://circleci.com/gh/vapor-ware/synse-server-grpc.svg?style=svg&circle-token=5c8fc7e65c9363a99cc224ee349ab7e72e39742c)](https://circleci.com/gh/vapor-ware/synse-server-grpc)

# synse-server-grpc
The internal gRPC API for Synse Server and its plugins.

## Overview
As of version 2.0, Synse Server uses a gRPC API internally to communicate with background
plugins to get information and readings to/from configured devices. This repo contains the
gRPC [API spec](api-spec) as well as auto-generated Python and Go packages for the gRPC
API client/server.

Since the gRPC API components are used in multiple places (e.g. Python client in Synse Server,
Go server in Plugins), this repo serves as the common location for the shared pieces.

## Building
If changes need to be made to the gRPC API, the `go/` and `python/` (and any future supported
language directory) should *not* be modified. Only the protobuf spec (synse.proto) should be 
modified. Once changed as desired, the language specific code can be generated via the make 
target:

```bash
make all
```

Additionally, packages for a supported language can be built by passing `make` the name of 
the language, e.g.

```bash
# auto-generate the python source
make python

# auto-generate the go source
make go
```

## Using

### Go
To use the generated client/server wrapper code for the gRPC API spec, you simply just need to 
get it as you would any other go package.

```bash
go get -v github.com/vapor-ware/synse-server-grpc/go
```

Then, it can be used in your project where necessary.

```go
package plugin

import (
    synse "github.com/vapor-ware/synse-server-grpc/go"
)
```

### Python
> TODO: The distribution mechanism here is not fully figured out yet. Still a work in progress. I think
> that it would make sense to build a python package tarball and upload that to GitHub as a release artifact
> where it could be downloaded and installed in a Dockerfile. For now, I'll assume that is the case, but it
> is liable to change.

The Python package can be installed as a tarball from GitHub under a particular release.

```bash
curl ...
tar -xzvf ...
```

Once you have the tarball, it can simply be installed via `pip`

```bash
pip3 install synse_plugin-*.tar.gz
```

You can then verify locally that it was installed 

```bash
python3 -c "import synse_plugin"
```

Alternatively, the Python source can be installed from a clone of this repo. The Makefile provides
targets to package, install, and uninstall via `pip`. It will do so for both Python 2 (assuming the
binary is named 'python') and Python 3 (assuming the binary is named 'python3').

```bash
# package the python code into a tarball
make pip-package

# install the packaged tarball (for development, see below)
make pip-install

# install the source in editable mode (recommended for development)
make pip-einstall

# uninstall synse_plugin from pip
make pip-uninstall

# clean up the artifacts generated from build/packaging
make pip-clean
``` 

## Releasing
To release a new version of Synse Server gRPC, you must have the correct permissions on the repo.
Assuming that you do, a few steps need to be taken. First, you need to know what version number is
to be released. Ideally, this should already be checked in to the repo. The version is currently
defined in `python/synse_plugin/__init__.py` under the `__version__` variable. 

The version can be verified by running 
```bash
make version
```

Then, clean out any of the previously build packages which may exist.
```bash
make pip-clean
```

Next, rebuild the packages. Make sure that the repo is up to date prior to this.
```bash
make pip-package
```

This should create the `python/dist` directory which contains a tarball with the version
number in the tarball name.

Finally, run
```bash
make release-github
```

This will build a docker image that will install `hub` and create a new release draft under
the specified version. It will include the python package tarball in the release distribution.

Once that is done, you can go to the [GitHub release page](release-page) and should see that a new release
draft was created. You can then edit this draft and publish it.


## Troubleshooting
To see a list of available make targets and a brief description, use
```bash
make help
```

If there is a bug or other issue you would like to report, please open a GitHub issue and provide
as much context around the bug/issue as possible.



[api-spec]: https://github.com/vapor-ware/synse-server-grpc/blob/master/synse.proto
[release-page]: https://github.com/vapor-ware/synse-server-grpc/releases
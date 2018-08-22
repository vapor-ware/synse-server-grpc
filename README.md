<p align="center"><a href="https://www.vapor.io/"><img src="assets/logo.png" width="360"></a></p>
<p align="center">
    <a href="https://circleci.com/gh/vapor-ware/synse-server-grpc"><img src="https://circleci.com/gh/vapor-ware/synse-server-grpc.svg?style=shield"></a>
    <a href="https://pypi.python.org/pypi/synse-grpc"><img src="https://img.shields.io/pypi/v/synse-grpc.svg"></a>
<a href="https://app.fossa.io/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.io/api/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc.svg?type=shield"/></a>
        
<h1 align="center">Synse GRPC</h1>
</p>

<p align="center">The internal gRPC API for Synse Server and its plugins.</p>


As of version 2.0, Synse Server uses a gRPC API internally to communicate with
plugins to get information and readings to/from configured devices. This repo contains the
gRPC [API spec][api-spec] as well as auto-generated Python and Go packages for the gRPC
API client/server.

Since the gRPC API components are used in multiple places (e.g. Python client in Synse Server,
Go server in Plugins), this repo serves as the common location for the shared pieces.

## The Synse Ecosystem
Synse Server is one component of the greater Synse Ecosystem.

- [**vapor-ware/synse-server**][synse-server]: An HTTP server providing a uniform API to interact
  with physical and virtual devices via plugin backends. This can be thought of as a 'front end'
  for Synse Plugins.
  
- [**vapor-ware/synse-sdk**][synse-sdk]: The official SDK (written in Go) for Synse Plugin
  development.

- [**vapor-ware/synse-cli**][synse-cli]: A CLI that allows you to easily interact with
  Synse Server and Plugins directly from the command line.

- [**vapor-ware/synse-graphql**][synse-graphql]: A GraphQL wrapper around Synse Server's
  HTTP API that provides a powerful query language enabling simple aggregations and
  operations over multiple devices.

- [**vapor-ware/synse-emulator-plugin**][synse-emulator]: A simple plugin with no hardware
  dependencies that can serve as a plugin backend for Synse Server for development,
  testing, and just getting familiar with how Synse Server works.


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
To use the generated client/server code for the Synse gRPC API, you simply just need to 
get it as you would any other go package.

```bash
go get -v github.com/vapor-ware/synse-server-grpc/go
```

It is then simple to import in a project.

```go
package plugin

import (
    synse "github.com/vapor-ware/synse-server-grpc/go"
)
```

### Python
To use the generated client/server code for the Synse gRPC API, you can get if from pypi
with pip

```bash
pip install synse-grpc
```

It is then simple to import in a project.

```python
import synse_grpc
```


## Releasing
GitHub releases are done via CI. The go source does not need to be published anywhere,
as it can be imported directly from this repo. The python source does need to be published.
A make target is provided to make it easy.

```bash
make py-publish
```


## Troubleshooting
To see a list of available make targets and a brief description, use
```bash
make help
```

If there is a bug or other issue you would like to report, please open a GitHub issue and provide
as much context around the bug/issue as possible.



[synse-server]: https://github.com/vapor-ware/synse-server
[synse-cli]: https://github.com/vapor-ware/synse-cli
[synse-emulator]: https://github.com/vapor-ware/synse-emulator-plugin
[synse-graphql]: https://github.com/vapor-ware/synse-graphql
[synse-sdk]: https://github.com/vapor-ware/synse-sdk


[api-spec]: https://github.com/vapor-ware/synse-server-grpc/blob/master/synse.proto
[release-page]: https://github.com/vapor-ware/synse-server-grpc/releases

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc?ref=badge_large)
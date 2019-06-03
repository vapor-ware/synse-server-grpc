# Synse gRPC

[![PyPI](https://img.shields.io/pypi/v/synse-grpc.svg)](https://pypi.python.org/pypi/synse-grpc)
[![Build](https://build.vio.sh/buildStatus/icon?job=vapor-ware/synse-server-grpc/master)](https://build.vio.sh/blue/organizations/jenkins/vapor-ware%2Fsynse-server-grpc/activity)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc?ref=badge_shield)

The internal [gRPC](https://grpc.io/docs/) API for the [Synse](https://github.com/vapor-ware/synse) platform.

This API enables bi-directional communication between [Synse Server](https://github.com/vapor-ware/synse-server)
and its registered data-providing plugins. This API is kept in its own repository
since it is used by multiple components written in different languages. This repo
contains:

- The Synse gRPC spec ([synse.proto](synse.proto))
- The auto-generated gRPC code for Go ([go/](go))
- The auto-generated gRPC code for Python with a simple client wrapper ([python/](python))

## Getting

### Go

```
go get github.com/vapor-ware/synse-server-gprc/go
```

### Python

```
pip install synse_grpc
```

## Developing

### Generating Language Sources

If changes need to be made to the gRPC API, it is important to ensure backwards compatibility
with the existing API spec. See the gRPC documentation for details on this. Additionally, the
files within the `go/` directory and the `synse_pb2.py` and `synse_pb2_grpc.py` files in the
`python/` directory are auto-generated and should **not** be modified manually. Instead, the
[protobuf](https://developers.google.com/protocol-buffers/) spec ([synse.proto](synse.proto))
should be modified and new source files should be generated. Makefile targets are provided to
make this simple:

```bash
make all
```

Source files for a single supported language may be built with the language-specific target,
e.g.

```bash
# auto-generate the Python source files
make python

# auto-generate the Go source files
make go
```

### Releasing

A new release is triggered by GitHub tag. The version of the release is defined in
`python/synse_grpc/__init__.py`. The version should follow the SemVer spec. Once a
corresponding tag is pushed (e.g. via `make github-tag`), CI will package, release,
and publish any artifacts.

Releasing and artifact publishing should not be done manually. 

### Troubleshooting

To see a list of available make targets and a brief description, use
```bash
make help
```

If there is a bug or other issue you would like to report, please open a GitHub issue and provide
as much context around the bug/issue as possible.

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fvapor-ware%2Fsynse-server-grpc?ref=badge_large)
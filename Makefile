
# Make GRPC client/server source files for the target languages
# -------------------------------------------------------------

python:
	docker run \
	    -v `pwd`:/build \
	    grpc/python:1.4 \
	    python -m grpc_tools.protoc -I/build --python_out=/build --grpc_python_out=/build /build/synse.proto


go:
	docker run \
	    -v `pwd`:/build \
	    grpc/go:1.0 \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build


.PHONY: python go
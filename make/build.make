
python:  ## Build the GRPC source for Python
	@printf "Generating Python source."
	@docker run \
	    -v `pwd`:/build \
	    grpc/python:1.4 \
	    python3 -m grpc_tools.protoc -I/build \
	        --python_out=/build/python/synse_plugin \
	        --grpc_python_out=/build/python/synse_plugin \
	        /build/synse.proto && \
	sed -i -e 's/import synse_pb2 as synse__pb2/from . import synse_pb2 as synse__pb2/g' python/synse_plugin/synse_pb2_grpc.py && \
	if [ -f "python/synse_plugin/synse_pb2_grpc.py-e" ]; then rm python/synse_plugin/synse_pb2_grpc.py-e; fi;
	@printf " [done]\n"



go:  ## Build the GRPC source for Go
	@printf "Generating Go source."
	@docker run \
	    -v `pwd`:/build \
	    grpc/go:1.0 \
	    protoc -I /build /build/synse.proto --go_out=plugins=grpc:/build/go
	@printf " [done]\n"


all: python go  ## Build source for all supported languages


.PHONY: all go python
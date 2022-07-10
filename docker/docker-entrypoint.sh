#!/bin/bash
set -e  # exit for nonzero codes (ie. nginx -t fails)

# NOTE all files and processes will inherit the user and groups
#   from the process starting this script
#   under normal circumstances, this will be root

echo "sourcing .bashrc"
source ~/.bashrc

pipenv run pip freeze

# generate the protobuff files to ensure they exist
pipenv run python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. src/protos/*.proto

# start the server
pipenv run python -m src.streamer_server

exec sleep infinity

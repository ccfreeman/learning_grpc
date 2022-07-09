#!/bin/bash
set -e  # exit for nonzero codes (ie. nginx -t fails)

# NOTE all files and processes will inherit the user and groups
#   from the process starting this script
#   under normal circumstances, this will be root

echo "sourcing .bashrc"
source ~/.bashrc

pipenv run pip freeze

# start gunicorn
pipenv run python -m src.server.greeter_server

exec sleep infinity

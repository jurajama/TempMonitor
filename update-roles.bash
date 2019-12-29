#!/usr/bin/env bash

# Install and/or update all roles
# --force is needed to do an update of installed roles :-/

ansible-galaxy install -r requirements.yml \
  -p ext-roles \
  --force \
  --verbose \
  --no-deps

#!/bin/bash

# This script creates a superuser for the cms with the username "root" and an empty email-field.
# It uses the settings for the postgres docker container and cannot be used with a standalone installation of postgres.

# Import utility functions
# shellcheck source=./tools/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/_functions.sh"

require_installed
require_database

integreat-cms-cli createsuperuser --verbosity "${SCRIPT_VERBOSITY}"

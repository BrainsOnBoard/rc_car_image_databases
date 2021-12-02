#!/bin/sh
set -e

# Requires that image_database_unwrapper (from bob_robotics/tools) is on PATH
find . -type d -name 'dataset*' -exec image_database_unwrapper {} -r 720 150 \;

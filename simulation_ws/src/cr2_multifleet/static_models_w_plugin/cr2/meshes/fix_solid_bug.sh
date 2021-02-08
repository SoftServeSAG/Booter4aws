#!/usr/bin/env bash

#  this script fixes the warning with 'solid' declaration in STL files.

sed -i 's/^solid/dilos/' body.STL
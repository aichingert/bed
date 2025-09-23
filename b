#!/bin/sh

set -e

clang -Wall -Wextra mob.c -o mob
./mob 
rm mob 
./bed_unit
rm bed_unit

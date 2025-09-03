#!/bin/sh

clang -DMOB_SELF_BUILD=1 -Wall -Wextra mob.c -o mob && ./mob && rm mob

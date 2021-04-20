#!/bin/sh -e

readonly this=$(readlink -f -- "$0")
readonly dir=$(dirname -- "$this")
readonly module=antp

cd -- "$dir" || exit

python3 -m "$module" "$@"

#!/bin/sh -e

readonly module=antp

if ! [ -d "$module" ]; then
	readonly this=$(readlink -f -- "$0")
	readonly dir=$(dirname -- "$this")
	cd -- "$dir" || exit 1
fi

python3 -m "$module" "$@"

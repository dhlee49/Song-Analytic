#!/bin/bash

ROOT="$(dirname "${BASH_SOURCE[0]}")"

cd "$ROOT"
source "$ROOT/pyinstall.sh"

[[ $# -gt 0 ]] && exec "$@"

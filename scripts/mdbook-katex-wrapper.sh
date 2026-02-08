#!/bin/sh

set -eu

err_file="$(mktemp)"
status=0

if ! mdbook-katex "$@" 2>"$err_file"; then
    status=$?
fi

if [ -s "$err_file" ]; then
    grep -v "This mdbook-katex was built against mdbook v" "$err_file" >&2 || true
fi

rm -f "$err_file"
exit "$status"

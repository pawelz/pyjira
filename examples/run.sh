#!/bin/sh

if [ "$#" = '0' ]; then
	2>&1 echo "Usage $0 name [args]"
	exit 1
fi

BASE=$(dirname $0)

if [ -r "$BASE/$1" ]; then
	SCRIPT="$BASE/$1"
elif [ -r "$BASE/$1.py" ]; then
	SCRIPT="$BASE/$1.py"
else
	2>&1 echo "Files not found: ‘$BASE/$1’ ‘$BASE/$1.py’"
	exit 1
fi

shift

PYTHONPATH="$BASE/.." python "$SCRIPT" ${1:+$@}

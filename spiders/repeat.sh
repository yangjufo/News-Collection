#!/bin/bash

# Determine directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Use virtualenv python if available, else python3
if [ -f "$DIR/../venv/bin/python" ]; then
    PYTHON="$DIR/../venv/bin/python"
elif [ -f "$DIR/../env/bin/python" ]; then
    PYTHON="$DIR/../env/bin/python"
else
    PYTHON="python3"
fi

$PYTHON news_spider.py "$@"

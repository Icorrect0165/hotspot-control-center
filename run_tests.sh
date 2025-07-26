#!/bin/bash
set -e

echo "Running pre-install tests..."
pytest --maxfail=1 --disable-warnings -v tests/ 
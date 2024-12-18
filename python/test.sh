#!/bin/sh
. .venv/bin/activate
cd test
PYTHONPATH=../src:../test uv run -- python -m unittest
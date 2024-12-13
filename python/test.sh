#!/bin/sh
cd test
PYTHONPATH=../src:../test uv run -- python -m unittest
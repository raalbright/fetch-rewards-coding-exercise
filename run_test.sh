#!/bin/bash
export PYTHONPATH=.
source $(pipenv --venv)/bin/activate
pytest -v
#! /usr/bin/env bash

PYTHONPATH=backend python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > openapi.json


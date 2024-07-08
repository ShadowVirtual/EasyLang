#!/bin/bash

pip install -r requirements.txt

exec env python src/main.py examples/example_code.txt
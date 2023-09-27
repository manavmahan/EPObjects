#! /bin/bash
flake8 --extend-ignore F401 ./probabilistic/*.py
flake8 --extend-ignore F401 ./tests/test_*.py

python3 -m unittest tests/test_*.py
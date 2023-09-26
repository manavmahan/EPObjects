#! /bin/bash
flake8 --extend-ignore F401 ./tests/*.py
flake8 --extend-ignore F401 ./probabilistic/*.py
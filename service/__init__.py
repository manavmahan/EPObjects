import json
import numpy as np
import os
import pandas as pd
import requests
import shutil

from logger import logger

tmp_dir = "/tmp/energy_service/"
os.makedirs(tmp_dir, exist_ok=True)
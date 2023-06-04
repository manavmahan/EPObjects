#!/usr/bin/python3
import sys
from service.service import run_service

if __name__ == '__main__':
    user_name = sys.argv[1]
    project_name = sys.argv[2]
    run_service(user_name, project_name)
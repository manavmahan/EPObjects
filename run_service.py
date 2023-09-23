#!/usr/bin/python3
import sys
from service.service import run_service
from logger import logging

if __name__ == '__main__':
    user_name = sys.argv[1]
    project_name = sys.argv[2]
    print ('Update Requested for:\t', user_name, project_name)
    run_service(user_name, project_name)
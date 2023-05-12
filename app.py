from flask import Flask
from flask import request

from pathlib import Path
home = str(Path.home())

import sys
path = f'{home}/repos/EPObjects/'
sys.path.insert(0, path)

from service.service import run_service

app = Flask(__name__)

@app.route("/")
def execute():
    api_id = request.args.get('api_id')
    if api_id != "6b504d93a5290653390d5f598c445f64":
        return "bad request"
    user_name = request.args.get('user_name')
    project_name = request.args.get('project_name')
    run_service(user_name, project_name)
    return f"updated User Name:{user_name} Project: {project_name}"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
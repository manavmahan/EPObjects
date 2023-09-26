from flask import Flask
from flask import request

from pathlib import Path
home = str(Path.home())

import sys
from flask_cors import cross_origin

path = f'{home}/repos/EPObjects/'
sys.path.insert(0, path)

from service.service import run_service

app = Flask(__name__)

@app.route("/", methods=['POST'])
@cross_origin()
def execute():
    request_data = request.get_json()
    api_id = request_data.get('api_id')
    if api_id != "6b504d93a5290653390d5f598c445f64":
        return "bad request"
    user_name = request_data.get('user_name')
    project_name = request_data.get('project_name')
    print (user_name, project_name)
    run_service(user_name, project_name)
    return f"updated User Name:{user_name} Project: {project_name}"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000, debug=True)
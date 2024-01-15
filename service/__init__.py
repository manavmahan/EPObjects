"""Module for service with flask app."""

from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from flask import request
import subprocess

from service import status

app = Flask(__name__)
talisman = Talisman(app, force_https=False)
CORS(app)

@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )

@app.route("/", methods=['POST'])
def execute():
    request_data = request.get_json()
    api_id = request_data.get('api_id')
    # if api_id != os.environ["API_ID"]:
    #     return "bad request"

    user_name = request_data.get('user_name')
    project_name = request_data.get('project_name')
    print (user_name, project_name)

    proc = subprocess.Popen(['python3', './run_service.py', user_name, project_name], 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    output = proc.stdout.read().decode("utf-8")
    errors = proc.stderr.read().decode("utf-8")

    if errors:
        return dict(output=output, errors=errors)
    return f"updated User Name:{user_name} Project: {project_name}"

# gunicorn --bind=0.0.0.0:7000 --log-level=info --timeout=3600 service:app

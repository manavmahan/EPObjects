"""Module for service."""
from .service import run_service

"""Flask app."""
import os
from flask import Flask, jsonify
from flask_talisman import Talisman
from flask_cors import CORS
from flask import request

from logger import logger
from service import run_service
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

    run_service(user_name, project_name)
    return {"message": f"updated User Name:{user_name} Project: {project_name}"}

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
# gunicorn --bind=0.0.0.0:7080 --log-level=info service:app

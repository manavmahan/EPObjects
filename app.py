"""Flask app."""
import os
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from flask import request
from flask_cors import cross_origin

from logger import logger
from service import run_service

app = Flask(__name__)
talisman = Talisman(app)
CORS(app)

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
# gunicorn --bind=0.0.0.0:8000 --log-level=info app:app

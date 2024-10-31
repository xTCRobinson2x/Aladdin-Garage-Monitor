from flask import Flask, request
from monitor import close_door_action
from logger import logger

app = Flask(__name__)
log = logger()


@app.route('/door/close', methods=['GET'])
def close_door():
    given_door_name = request.args.get("door_name")
    if not given_door_name:
        return "Door name is required", 400
    return close_door_action(given_door_name)

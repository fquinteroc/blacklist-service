from flask import Flask, jsonify

from src.blueprints.blacklists import blacklist_blueprint
from src.errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(blacklist_blueprint)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200


@app.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response


if __name__ == "__main__":
    app.run(debug=True)

from typing import TYPE_CHECKING
import os
import logging

from flask import Flask, render_template, request, jsonify

from sender import send_msg

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage

# configure application
flask_app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@flask_app.route("/")
def index():
    return render_template("index.html", msg="")


@flask_app.route("/infer_model", methods=["GET"])
def infer_model():
    """Send the request to the RabbitMQ."""
    try:
        command = 'start_model'
        flask_app.logger.info(command)
        send_msg(command, flask_app.logger)

        return jsonify({"status": "Successfully sent file"})
    except Exception as exc:
        flask_app.logger.error(exc)
        return jsonify({"status": "Sending the request failed"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5010))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)

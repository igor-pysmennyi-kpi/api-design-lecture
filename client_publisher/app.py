from typing import TYPE_CHECKING
import os
import logging
import threading

from flask import Flask, render_template, request, jsonify

from sender import send_msg
from listen_queue import listen_queue

# configure application
flask_app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


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
    

@flask_app.route("/get_result", methods=["GET"])
def get_result():
    """Get the result message from the RabbitMQ."""
    try:
        thread = threading.Thread(target=listen_queue, args=('flask_app.logger',))
        thread.start()
        thread.join()
        return jsonify(message=flask_app.config.get('MESSAGE', 'No message received'))

    except Exception as exc:
        flask_app.logger.error(exc)
        return jsonify({"status": "Sending the request failed"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5010))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)

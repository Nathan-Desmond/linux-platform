import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

# Version is passed in from outside (Docker / Ansible), defaults to "dev"
APP_VERSION = os.environ.get("APP_VERSION", "dev")


@app.route("/")
def index():
    return jsonify(
        message="Hello from the Linux Platform Homelab",
        hostname=socket.gethostname(),
        version=APP_VERSION,
        time=datetime.now(timezone.utc).isoformat(),
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    # Only used when running locally for testing
    app.run(host="0.0.0.0", port=5000)

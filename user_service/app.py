from flask import Flask, jsonify
from consul_registration import register_user_service

app = Flask(__name__)


@app.route('/users/<user_id>')
def get_user(user_id):
    return jsonify({"user_id": user_id, "name": "Hello World"})


@app.route('/health')
def health():
    return "User Service is healthy", 200


if __name__ == '__main__':
    register_user_service()
    app.run(port=5001)

from flask import Flask, jsonify
import consul

app = Flask(__name__)


# Register the User service with Consul
def register_with_consul():
    client = consul.Consul()
    service_id = "user-service-1"
    client.agent.service.register(
        name="user-service",
        service_id=service_id,
        port=5001,
        address="127.0.0.1",
        check=consul.Check.http("http://127.0.0.1:5001/health", interval="10s")
    )


@app.route('/users/<user_id>')
def get_user(user_id):
    return jsonify({"user_id": user_id, "name": "John Doe"})


@app.route('/health')
def health():
    return "User Service is healthy", 200


if __name__ == '__main__':
    register_with_consul()
    app.run(port=5001)

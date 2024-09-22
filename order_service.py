from flask import Flask, jsonify, request
import requests
import consul

app = Flask(__name__)


# Register the Order service with Consul
def register_with_consul():
    client = consul.Consul()
    service_id = "order-service-1"
    client.agent.service.register(
        name="order-service",
        service_id=service_id,
        port=5003,
        address="127.0.0.1",
        check=consul.Check.http("http://127.0.0.1:5003/health", interval="10s")
    )


def discover_service(service_name):
    client = consul.Consul()
    index, services = client.catalog.service(service_name)
    if services:
        service = services[0]
        return f"http://{service['ServiceAddress']}:{service['ServicePort']}"
    return None


@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get("user_id")
    product_id = request.json.get("product_id")

    # Discover the User Service
    user_service_url = discover_service("user-service")
    if user_service_url:
        user_response = requests.get(f"{user_service_url}/users/{user_id}")
        user_data = user_response.json()
    else:
        return "User Service not found", 500

    # Discover the Product Service
    product_service_url = discover_service("product-service")
    if product_service_url:
        product_response = requests.get(f"{product_service_url}/products/{product_id}")
        product_data = product_response.json()
    else:
        return "Product Service not found", 500

    # Create an order with user and product information
    order = {
        "order_id": "12345",
        "user": user_data,
        "product": product_data
    }

    return jsonify(order)


@app.route('/health')
def health():
    return "Order Service is healthy", 200


if __name__ == '__main__':
    register_with_consul()
    app.run(port=5003)

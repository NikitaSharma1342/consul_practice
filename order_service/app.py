from flask import Flask, jsonify, request
import requests
from consul_registration import register_order_service
from service_discovery import get_user_service_url, get_product_service_url

app = Flask(__name__)


@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get("user_id")
    product_id = request.json.get("product_id")

    user_service_url = get_user_service_url()
    if not user_service_url:
        return "User Service not found", 500

    product_service_url = get_product_service_url()
    if not product_service_url:
        return "Product Service not found", 500

    user_response = requests.get(f"{user_service_url}/users/{user_id}")
    user_data = user_response.json()

    product_response = requests.get(f"{product_service_url}/products/{product_id}")
    product_data = product_response.json()

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
    register_order_service()
    app.run(port=5003)

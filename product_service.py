from flask import Flask, jsonify
import consul

app = Flask(__name__)


# Register the Product service with Consul
def register_with_consul():
    client = consul.Consul()
    service_id = "product-service-1"
    client.agent.service.register(
        name="product-service",
        service_id=service_id,
        port=5002,
        address="127.0.0.1",
        check=consul.Check.http("http://127.0.0.1:5002/health", interval="10s")
    )


@app.route('/products/<product_id>')
def get_product(product_id):
    return jsonify({"product_id": product_id, "name": "Sample Product", "price": 20})


@app.route('/health')
def health():
    return "Product Service is healthy", 200


if __name__ == '__main__':
    register_with_consul()
    app.run(port=5002)

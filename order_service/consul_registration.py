from common.consul_helper import register_service


def register_order_service():
    service_name = "order-service"
    service_id = "order-service-1"
    service_port = 5003
    health_url = f"http://127.0.0.1:{service_port}/health"
    register_service(service_name, service_id, service_port, health_url)

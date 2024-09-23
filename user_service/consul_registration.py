from common.consul_helper import register_service


def register_user_service():
    service_name = "user-service"
    service_id = "user-service-1"
    service_port = 5001
    health_url = f"http://127.0.0.1:{service_port}/health"
    register_service(service_name, service_id, service_port, health_url)

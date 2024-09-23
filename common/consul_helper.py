import consul


def register_service(service_name, service_id, service_port, health_url):
    client = consul.Consul()
    client.agent.service.register(
        name=service_name,
        service_id=service_id,
        port=service_port,
        address="127.0.0.1",
        check=consul.Check.http(health_url, interval="10s")
    )


def discover_service(service_name):
    client = consul.Consul()
    index, services = client.catalog.service(service_name)
    if services:
        service = services[0]
        return f"http://{service['ServiceAddress']}:{service['ServicePort']}"
    return None
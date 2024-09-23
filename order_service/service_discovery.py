from common.consul_helper import discover_service


def get_user_service_url():
    return discover_service("user-service")


def get_product_service_url():
    return discover_service("product-service")

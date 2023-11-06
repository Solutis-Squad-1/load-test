from locust import HttpUser, between

from catalog import CatalogGetRouteLoadTest, CatalogSequentialRouteLoadTest


class WebsiteUser(HttpUser):
    tasks = [
        CatalogGetRouteLoadTest,
        CatalogSequentialRouteLoadTest,
    ]
    wait_time = between(1, 2)

from locust import HttpUser, between

from catalog import CatalogGetRouteLoadTest, CatalogSequentialRouteLoadTest
from identity import UserAuthSequentialRouteLoadTest, FindAllUsersRouteLoadTest


class WebsiteUser(HttpUser):
    tasks = [
        CatalogGetRouteLoadTest,
        CatalogSequentialRouteLoadTest,
        UserAuthSequentialRouteLoadTest,
        FindAllUsersRouteLoadTest
    ]
    wait_time = between(1, 2)

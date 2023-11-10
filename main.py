from locust import HttpUser, between

from catalog import CatalogGetRouteLoadTest, CatalogSequentialRouteLoadTest
from identity import UserAuthSequentialRouteLoadTest, FindAllUsersRouteLoadTest
from order import OrderGetRouteLoadTest, OrderSequentialRouteLoadTest


class WebsiteUser(HttpUser):
    tasks = [
        CatalogGetRouteLoadTest,
        CatalogSequentialRouteLoadTest,
        UserAuthSequentialRouteLoadTest,
        FindAllUsersRouteLoadTest,
        OrderGetRouteLoadTest,
        OrderSequentialRouteLoadTest
    ]
    wait_time = between(1, 2)

from locust import HttpUser, between

from catalog import CatalogGetRouteLoadTest, CatalogSequentialRouteLoadTest
from identity import UserAuthSequentialRouteLoadTest, FindAllUsersRouteLoadTest
from order import OrderGetRouteLoadTest, OrderSequentialRouteLoadTest
from payment import PaymentGetRouteLoadTest, PaymentSequentialRouteLoadTest


class WebsiteUser(HttpUser):
    tasks = [
        CatalogGetRouteLoadTest,
        CatalogSequentialRouteLoadTest,
        UserAuthSequentialRouteLoadTest,
        FindAllUsersRouteLoadTest,
        OrderGetRouteLoadTest,
        OrderSequentialRouteLoadTest,
        PaymentGetRouteLoadTest,
        PaymentSequentialRouteLoadTest
    ]
    wait_time = between(1, 2)

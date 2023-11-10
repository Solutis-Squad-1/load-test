from random import random
from faker import Faker
from locust import TaskSet, task, SequentialTaskSet
import os
from dotenv import load_dotenv

load_dotenv()

url = "/orders"


class OrderGetRouteLoadTest(TaskSet):
    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def list_all_orders(self):
        self.client.get(
            url,
            name="List all orders - Order"
        )


class OrderSequentialRouteLoadTest(SequentialTaskSet):
    faker = Faker()
    order_res = None

    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def create_order(self):
        res = self.client.post(
            url,
            json={
                "userId": 1,
                "summary": self.faker.text(),
                "items": [
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    },
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    },
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    }
                ]
            },
            name="Create order - Order"
        )
        self.order_res = res.json()

    @task
    def list_order_by_id(self):
        self.client.get(
            url + "/" + str(self.order_res['id']),
            name="List order by id - Order"
        )

    @task
    def list_all_orders_from_user(self):
        self.client.get(
            url + "/users/" + str(self.order_res['userId']),
            name="List all orders from user - Order"
        )

    @task
    def update_order(self):
        self.client.put(
            url + "/" + str(self.order_res['id']),
            json={
                "summary": self.faker.text(),
                "items": [
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    },
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    },
                    {
                        "productId": int(random() * 100 + 1),
                        "quantity": int(random() * 10 + 1),
                        "price": int(random() * 100 + 1)
                    }
                ],
                "status": "IN_PROCESSING"
            },
            name="Update order - Order"
        )

    @task
    def delete_order(self):
        self.client.delete(
            url + "/" + str(self.order_res['id']),
            name="Delete order - Order"
        )

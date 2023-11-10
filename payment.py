from random import random
from faker import Faker
from locust import TaskSet, task, SequentialTaskSet
import os
from dotenv import load_dotenv

load_dotenv()

url = "/payments"


class PaymentGetRouteLoadTest(TaskSet):
    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def list_all_payments(self):
        self.client.get(
            url,
            name="List all payments - Payment"
        )


class PaymentSequentialRouteLoadTest(SequentialTaskSet):
    faker = Faker()
    payment_res = None

    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def create_payment(self):
        res = self.client.post(
            url,
            json={
                "orderId": int(random() * 100 + 1),
                "userId": int(random() * 100 + 1),
                "total": float(random() * 100 + 1),
                "formPayment": "CREDIT_CARD",
            },
            name="Create payment - Payment"
        )
        self.payment_res = res.json()

    @task
    def list_order_by_id(self):
        self.client.get(
            url + "/" + str(self.payment_res['id']),
            name="List payment by id - Payment"
        )

    @task
    def update_order(self):
        self.client.put(
            url + "/" + str(self.payment_res['id']),
            json={
                "total": float(random() * 100 + 1),
                "formPayment": "PIX",
            },
            name="Update payment - Payment"
        )

    @task
    def delete_order(self):
        self.client.delete(
            url + "/" + str(self.payment_res['id']),
            name="Delete payment - Payment"
        )

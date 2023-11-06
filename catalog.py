from random import random
from faker import Faker
from locust import TaskSet, task, SequentialTaskSet
import os
from dotenv import load_dotenv

load_dotenv()


class CatalogGetRouteLoadTest(TaskSet):
    @task
    def list_all_products(self):
        self.client.get(
            "/catalog/products",
            name="List all products - Catalog"
        )

    @task
    def list_all_products_from_seller(self):
        self.client.get(
            "/catalog/products/sellers/1",
            name="List all products from seller - Catalog"
        )

    @task
    def list_all_categories(self):
        self.client.get(
            "/catalog/categories",
            name="List all categories - Catalog"
        )


class CatalogSequentialRouteLoadTest(SequentialTaskSet):
    faker = Faker()
    product_res = None
    category_res = None

    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def create_category(self):
        res = self.client.post(
            "/catalog/categories",
            json={
                "name": self.faker.name()
            },
            name="Create category - Catalog"
        )
        self.category_res = res.json()

    @task
    def list_category_by_id(self):
        self.client.get(
            "/catalog/categories/" + str(self.category_res['id']),
            name="List category by id - Catalog"
        )

    @task
    def create_product(self):
        res = self.client.post(
            "/catalog/products",
            json={
                "name": f"Test {self.faker.first_name()}",
                "description": f"Test {self.faker.first_name()}",
                "price": int(random() * 500),
                "sellerId": int(random() * 10) + 1,
                "categoryIds": [
                    self.category_res['id']
                ]
            },
            name="Create product - Catalog"
        )
        self.product_res = res.json()

    @task
    def list_product_by_id(self):
        self.client.get(
            "/catalog/products/" + str(self.product_res['id']),
            name="List product by id - Catalog"
        )

    @task
    def update_product(self):
        self.client.put(
            "/catalog/products/" + str(self.product_res['id']),
            json={
                "name": f"Test {self.faker.first_name()}",
                "description": f"Test {self.faker.first_name()}",
                "price": int(random() * 500),
                "sellerId": int(random() * 10) + 1,
                "categoryIds": [
                    self.category_res['id']
                ]
            },
            name="Update product - Catalog"
        )

    @task
    def delete_product(self):
        self.client.delete(
            "/catalog/products/" + str(self.product_res['id']),
            name="Delete product - Catalog"
        )

    @task
    def update_category(self):
        self.client.put(
            "/catalog/categories/" + str(self.category_res['id']),
            json={
                "name": self.faker.name()
            },
            name="Update category - Catalog"
        )

    @task
    def delete_category(self):
        self.client.delete(
            "/catalog/categories/" + str(self.category_res['id']),
            name="Delete category - Catalog"
        )

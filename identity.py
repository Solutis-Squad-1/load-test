from locust import SequentialTaskSet, task, TaskSet
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()


class FindAllUsersRouteLoadTest(TaskSet):
    def on_start(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + os.getenv('token'),
            'User-name': 'Test',
            'User-authorities': os.getenv('authorities')
        }

    @task
    def find_all_users(self):
        self.client.get(
            "/identity/users",
            name="Find all users - Identity"
        )


class UserAuthSequentialRouteLoadTest(SequentialTaskSet):
    faker = Faker()
    register_res = None
    login_res = None

    @task
    def register(self):
        res = self.client.post(
            "/identity/auth/register",
            json={
                "username": f"test {self.faker.first_name()} {self.faker.first_name()} {self.faker.first_name()}",
                "email": f"test{self.faker.first_name().strip()}@test.com",
                "password": "test",
            },
            name="Register - Identity"
        )

        self.register_res = res.json()

    @task
    def login(self):
        res = self.client.post(
            "/identity/auth/login",
            json={
                "username": str(self.register_res['username']),
                "password": "test",
            },
            name="Login - Identity"
        )

        self.login_res = res.json()

    @task
    def validate_token(self):
        self.client.post(
            "/identity/auth/validate",
            json={
                "token": str(self.login_res['token']),
            },
            name="Validate Token - Identity"
        )

    @task
    def find_user_by_id(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + str(self.login_res['token']),
        }
        self.client.get(
            "/identity/users/details",
            name="Find user by id - Identity"
        )

    @task
    def update_user(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + str(self.login_res['token']),
        }
        self.client.put(
            "/identity/users",
            json={
                "email": f"test{self.faker.first_name().strip()}@test.com",
                "address": {
                    "street": f"{self.faker.street_name()}",
                    "city": f"{self.faker.city()}",
                    "number": int(self.faker.building_number()),
                    "complement": f"{self.faker.street_suffix()}",
                    "neighborhood": f"{self.faker.city_suffix()}",
                    "zipCode": f"{self.faker.postcode()}"
                }
            },
            name="Update user by id - Identity"
        )

    @task
    def delete_user(self):
        self.client.headers = {
            'Authorization': 'Bearer ' + str(self.login_res['token']),
        }
        self.client.delete(
            "/identity/users",
            name="Delete user by id - Identity"
        )

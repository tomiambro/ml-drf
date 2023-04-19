import logging
import random

from locust import HttpUser, task

input_data = [
    17.99,
    10.38,
    122.8,
    1001,
    0.1184,
    0.2776,
    0.3001,
    0.1471,
    0.2419,
    0.07871,
    1.095,
    0.9053,
    8.589,
    153.4,
    0.006399,
    0.04904,
    0.05373,
    0.01587,
    0.03003,
    0.006193,
    25.38,
    17.33,
    184.6,
    2019,
    0.1622,
    0.6656,
    0.7119,
    0.2654,
    0.4601,
    0.1189,
]


class WebUser(HttpUser):
    user_data = {"username": "locust", "password": "locust"}

    def on_start(self):
        # Create a new user
        response = self.client.post("/api/users/register/", self.user_data)
        if response.status_code == 201:
            logging.info("User created successfully")
        else:
            logging.error(response.json())
            raise Exception("Cannot create user")

        # Perform authentication
        response = self.client.post("/auth-token/", self.user_data)
        if response.status_code == 200:
            # Save the token in the session
            self.client.headers["Authorization"] = "Token " + response.json()["token"]
            logging.info("User authenticated successfully")
        else:
            # Authentication failed, raise an exception
            logging.error(response.json())
            raise Exception("Failed to authenticate")

    @task
    def test_home_page(self):
        self.client.get("/")

    @task
    def test_infer_endpoint(self):
        input = [round(x + random.random(), 2) for x in input_data]
        input = random.choice([input, 0])
        data = {"input": input}
        res = self.client.post("/core/infer", data)
        assert res.status_code == 200

    def on_stop(self):
        # Delete the recently created user
        response = self.client.delete("/api/users/locust/")
        if response.status_code == 204:
            logging.info("User deleted successfully")
        else:
            logging.error(response.json())
            raise Exception("Cannot delete user")

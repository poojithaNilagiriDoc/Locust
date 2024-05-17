import time
from locust import HttpUser, task, between
import random
import json

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # @task
    # def index_page(self):
    #     self.client.get(url="/hello")

    @task
    def slow_page(self):
        response = self.client.get(url="/api/users/2")
        if response.status_code != 200:
            print(f"Error: GET request failed - Status code: {response.status_code}")

    # @task
    # def post_data(self):
    #     headers = {'Content-Type': 'application/json'}  # Adjust headers as needed
    #     payload = {
    #         "name": "morpheus",
    #         "job": "leader"
    #     }
    #     response = self.client.post("/api/users", json=payload, headers=headers)
    #     if response.status_code != 201:
    #         print(f"Error: POST request failed - Status code: {response.status_code}")

    # @task
    # def post_data_Random(self):
    #     headers = {'Content-Type': 'application/json'}
    #     names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    #     payload = {
    #         "name": random.choice(names),
    #         "job": "leader"
    #     }
    #     response = self.client.post("/api/users", json=payload, headers=headers)
    #     if response.status_code == 201:
    #         print(response.text)
    #     if response.status_code != 201:
    #         print(f"Error: POST request failed - Status code: {response.status_code}")

    # You can define more tasks to simulate various user behaviors

    @task
    def my_task(self):
        headers = {'Content-Type': 'application/json'}
        names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        payload = {
            "name": random.choice(names),
            "job": "leader"
        }
        response = self.client.post("/api/users", json=payload, headers=headers)
        if response.status_code == 200:
            self.environment.events.request_success.fire(
                request_type="POST",
                name="/api/users",
                response_time=response.elapsed.total_seconds(),
                response_length=len(response.content),
            )
        else:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/api/users",
                response_time=response.elapsed.total_seconds(),
                exception=None,
            )

    def on_stop(self):
        successful_responses = []
        for name, stats in self.environment.stats.entries.items():
            if name == '/api/users' and 'POST' in stats:
                for request in stats['POST'].requests:
                    if request.response.status_code == 200:
                        successful_responses.append(request.response)
        
        print("Successful POST responses:")
        for response in successful_responses:
            print(f"Response: {response.text}")

        # You can log or perform any other actions with the successful responses

from locust import HttpUser, task, between


class RateLimitUser(HttpUser):

    wait_time = between(0.1, 1)

    @task
    def test_api(self):
        self.client.get("/api/data")
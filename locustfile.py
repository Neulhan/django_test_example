from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def get_list_action(self):
        self.client.get("/api/news/")

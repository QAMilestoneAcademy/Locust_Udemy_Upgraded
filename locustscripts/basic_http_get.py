from locust import HttpUser,task,between

class MyUser(HttpUser):

    wait_time=between(1,2)
    host="http://newtours.demoaut.com"

    @task
    def launch_URL(self):
        self.client.get("/mercurycruise.php",name="viewcruise")

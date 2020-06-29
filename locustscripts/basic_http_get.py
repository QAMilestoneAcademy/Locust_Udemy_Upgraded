from locust import HttpUser,task,between

class MyUser(HttpUser):

    connection_timeout = 60.0
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"

    @task
    def launch_URL(self):
        res=self.client.get("/mercurycruise.php",name="viewcruise")



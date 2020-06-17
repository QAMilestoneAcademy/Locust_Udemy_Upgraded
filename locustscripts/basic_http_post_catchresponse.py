from locust import HttpUser,SequentialTaskSet,task,between

class UserBehaviour(SequentialTaskSet):

    @task
    def launch_URL(self):
        with self.client.get("/mercurysignon.php", name="launchmercury",catch_response=True) as resp1:
            if("Mercury Tours") in resp1.text:
                resp1.success()
            else:
                resp1.failure("failed to launch url")

    @task
    def login(self):
        with self.client.post("/login.php", name="login", data={"action": "process","userName": "qamile1@gmail.com",
                                                           "password": "qamile","login.x": "41","login.y": "12"}, catch_response=True) as resp2:

            if ("Find a Flights") in resp2.text:
                resp2.success()
            else:
                resp2.failure("failed to login")


class MyUser(HttpUser):
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]

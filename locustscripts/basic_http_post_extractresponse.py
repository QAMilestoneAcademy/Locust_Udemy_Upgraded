from locust import HttpUser,SequentialTaskSet,task,between

class UserBehaviour(SequentialTaskSet):

    @task
    def launch_URL(self):
        resp1=self.client.get("/mercurysignon.php", name="launchmercury")
        print(resp1.text)
        print(resp1.status_code)
        print(resp1.headers)

    @task
    def login(self):
        resp2=self.client.post("/login.php", name="login", data={"action": "process","userName": "qamile1@gmail.com",
                                                           "password": "qamile","login.x": "41","login.y": "12"})
        print(resp2.text)
        print(resp2.status_code)
        print(resp2.headers)

class MyUser(HttpUser):
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]

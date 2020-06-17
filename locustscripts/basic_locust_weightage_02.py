from locust import User,task,between

class MyWebUser(User):
    wait_time=between(1,2)
    weight =3
    @task
    def login_URL(self):
     print("I am loggin into web URL")

class MyMobileUser(User):
    wait_time=between(1,2)
    weight = 1
    @task
    def login_URL(self):
     print("I am loggin into mobile URL")
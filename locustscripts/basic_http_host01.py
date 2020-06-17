from locust import HttpUser,task,between

class MyUser(HttpUser):

    wait_time=between(1,2)
    host="http://newtours.demoaut.com/"

    @task
    def login_URL(self):
     print("I am loggin into URL")
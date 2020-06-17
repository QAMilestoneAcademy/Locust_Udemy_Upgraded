from locust import User,task,between

class MyUser(User):

    wait_time=between(1,2)


    def on_start(self):
     print("I am loggin into URL")

    @task
    def doing_work(self):
     print("I am doing my work")


    def on_stop(self):
         print("I am logging out")
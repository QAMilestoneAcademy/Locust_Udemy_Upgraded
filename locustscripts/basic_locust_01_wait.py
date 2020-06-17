from locust import User,task,between,constant,constant_pacing
from datetime import datetime

class MyUser(User):

    # wait_time=between(1,3)
    # wait_time=constant(3)
    wait_time = constant_pacing(5)

    @task
    def login_URL(self):
     print(datetime.now())
from locust import HttpUser,SequentialTaskSet,task,between

class UserBehaviour(SequentialTaskSet):

    def on_start(self):
        with self.client.post("/login.php", name="login", data={"action": "process","userName": "qamile1@gmail.com",
                                                           "password": "qamile","login.x": "41","login.y": "12"}, catch_response=True) as resp:

            if ("Find a Flight") in resp.text:
                resp.success()
            else:
                resp.failure("failed to login")
    @task()
    def find_flight(self):
        print("add post request to search flight")
        print("verify with catch response that flight search is successful")
        #Select a Flight


    @task()
    def select_flight(self):
        print("add post request to select flight")
        print("verify with catch response that select flight is successful")
        #Book a Flight

    @task()
    def book_flight(self):
        print("add post request to book flight")
        print("verify with catch response that flight book is successful")
        print("once success criteria is met, you can change criteria to wrong wordings to see fail criteria is working")
        #Flight Confirmation

class MyUser(HttpUser):
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]

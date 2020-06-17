from locust import User,SequentialTaskSet,task,between

class UserBehaviour(SequentialTaskSet):

 def on_start(self):
     print("I will login")


 @task()
 def find_flight(self):
    print("I will find flight by entering criteria")

 @task()
 def select_flight(self):
  print("select_flight")

 @task()
 def book_flight(self):
  print("book_flight")

class MyUser(User):
    wait_time=between(1,2)
    tasks=[UserBehaviour]


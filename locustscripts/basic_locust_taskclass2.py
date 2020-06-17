from locust import User,TaskSet,task,between

class MyUser(User):
    wait_time=between(1,2)

    @task()
    class UserBehaviour(TaskSet):
        @task()
        def add_cart(self):
            print("I am add to cart")

        @task()
        def view_product(self):
            print("I am view product")


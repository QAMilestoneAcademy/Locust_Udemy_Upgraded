from locust import task,HttpUser,SequentialTaskSet,between

class UserBehaviour(SequentialTaskSet):

    def __init__(self,parent):
        super().__init__(parent)
        self.jsession_id=""
        self.userfilter_session_id = ""

    def on_start(self):
        print("I will launch URL")
        res=self.client.get("/InsuranceWebExtJS/index.jsf",name="launchURL")
        self.jsession_id=res.cookies["JSESSIONID"]
        print("I will retrieve cookie" +self.jsession_id)
        print("I will login + using cookie jsessionid" + self.jsession_id)
        with self.client.post("/InsuranceWebExtJS/index.jsf"
                , data={"login-form": "login-form", "login-form:email": "qamile2@gmail.com"
                    , "login-form:password": "abc123", "login-form:login.x": "57"
                    , "login-form:login.y": "9", "javax.faces.ViewState": "j_id1:j_id2"}
                , cookies={"JSESSIONID": self.jsession_id}, name="login", catch_response=True) as res:
            if ("Logged in") not in res.text:
                res.failure("User not logged in")
            else:
                res.success()
                print("user is logged in...")


    @task()
    def select_autoquote(self):
        print("I am selecting autoquote+ using 2 cookies jsessionid + usersessionfilter" + self.jsession_id)
        print("I am selecting autoquote+ using 2 cookies usersessionfilter")

class MyUser(HttpUser):
    tasks=[UserBehaviour]
    wait_time=between(2,4)
    host="http://demo.borland.com"
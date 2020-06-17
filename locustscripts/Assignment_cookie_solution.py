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
                , cookies={"JSESSIONID": self.jsession_id}, name="login", catch_response=True) as res1:
            if ("Logged in") not in res1.text:
                res1.failure("User not logged in")
            else:

                res1.success()
                print("user is logged in...")
                self.userfilter_session_id = res1.cookies['UserSessionFilter.sessionId']

    @task()
    def select_autoquote(self):
        with self.client.get("/InsuranceWebExtJS/quote_auto.jsf",name="select_autoquote", cookies={'JSESSIONID': self.jsession_id,
                                                                           'UserSessionFilter.sessionId':
                                                                               self.userfilter_session_id},
                             catch_response=True) as res2:

            if "Get Instant Auto Quote" not in res2.text:
                print("I am in res2 one")
                res2.failure("Got wrong response")
            else:
                print("I am in res2 two")
                res2.success()

class MyUser(HttpUser):
    tasks=[UserBehaviour]
    wait_time=between(2,4)
    host="http://demo.borland.com"
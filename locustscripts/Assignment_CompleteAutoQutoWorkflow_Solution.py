from locust import task, HttpUser, SequentialTaskSet, between
import re


class UserBehaviour(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.jsession_id = ""
        self.userfilter_session_id = ""
        self.viewstate = ""

    def on_start(self):
        print("I will launch URL")
        res = self.client.get("/InsuranceWebExtJS/index.jsf", name="launchURL", headers={"Cache-Control": "no-cache"})
        self.jsession_id = res.cookies["JSESSIONID"]
        # "j_id1:j_id2"
        re1 = re.findall("j_id\d+:j_id\d+", res.text)
        self.viewstate = re1[0]

        with self.client.post("/InsuranceWebExtJS/index.jsf"
                , data={"login-form": "login-form", "login-form:email": "qamile2@gmail.com"
                    , "login-form:password": "abc123", "login-form:login.x": "57"
                    , "login-form:login.y": "9", "javax.faces.ViewState": self.viewstate}
                , cookies={"JSESSIONID": self.jsession_id}, name="login", catch_response=True) as res1:
            if ("Logged in") not in res1.text:
                res1.failure("User not logged in")
            else:

                res1.success()
                self.userfilter_session_id = res1.cookies['UserSessionFilter.sessionId']
                re1 = re.findall("j_id\d+:j_id\d+", res.text)
                self.viewstate = re1[0]
                print("viewstat2" + self.viewstate)

    @task()
    def select_autoquote(self):
        with self.client.get("/InsuranceWebExtJS/quote_auto.jsf", name="select_autoquote",
                             cookies={'JSESSIONID': self.jsession_id,
                                      'UserSessionFilter.sessionId':
                                          self.userfilter_session_id},
                             catch_response=True) as res2:

            if "Get Instant Auto Quote" not in res2.text:
                res2.failure("Got wrong response")
            else:
                res2.success()
                re1 = re.findall("j_id\d+:j_id\d+", res2.text)
                self.viewstate = re1[0]

    # Assignment --Complete autoquote workflow by adding task for each step, catch_response & validate, extract view state at each request
    @task()
    def getinstantquote_1(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto.jsf", name="getinstantquote_1",data={"autoquote": "autoquote",
                                                                         "autoquote:zipcode": "00000000",
                                                                         "autoquote:e-mail": "qamile2@gmail.com",
                                                                         "autoquote:vehicle": "car",
                                                                         "autoquote:next.x": "38",
                                                                         "autoquote:next.y": "10",
                                                                         "javax.faces.ViewState": self.viewstate},
                              cookies={'JSESSIONID': self.jsession_id,
                                       'UserSessionFilter.sessionId':
                                           self.userfilter_session_id},
                              catch_response=True) as res4:

            if "You're almost done" not in res4.text:
                res4.failure("Got wrong response")
                print(res4.text)
            else:
                res4.success()
                re1 = re.findall("j_id\d+:j_id\d+", res4.text)
                self.viewstate = re1[0]

    @task()
    def getinstantquote_2(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto2.jsf", name="getinstantquote_2",data={"autoquote": "autoquote",
                                                                          "autoquote:age": "0",
                                                                          "autoquote:gender": "Male",
                                                                          "autoquote:type": "Excellent",
                                                                          "autoquote:next.x": "35",
                                                                          "autoquote:next.y": "7",
                                                                          "javax.faces.ViewState": self.viewstate},
                              cookies={'JSESSIONID': self.jsession_id,
                                       'UserSessionFilter.sessionId':
                                           self.userfilter_session_id},
                              catch_response=True) as res5:

            if "Last Screen" not in res5.text:
                res5.failure("Got wrong response")
            else:
                res5.success()
                re1 = re.findall("j_id\d+:j_id\d+", res5.text)
                self.viewstate = re1[0]

    @task()
    def getinstantquote(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto3.jsf", name="getinstantquote",data={"autoquote": "autoquote",
                                                                          "autoquote:year": "2008",
                                                                          "makeCombo": "Chrysler",
                                                                          "autoquote:make": "Chrysler",
                                                                          "modelCombo": "Aspen",
                                                                          "autoquote:model": "Aspen",
                                                                          "autoquote:finInfo": "Own",
                                                                          "autoquote:next.x": "26",
                                                                          "autoquote:next.y": "9",
                                                                          "javax.faces.ViewState": self.viewstate},
                              cookies={'JSESSIONID': self.jsession_id,
                                       'UserSessionFilter.sessionId':
                                           self.userfilter_session_id},
                              catch_response=True) as res6:

            if "Your Instant Quote is" not in res6.text:
                res6.failure("Got wrong response")
            else:
                res6.success()


class MyUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(2, 4)
    host = "http://demo.borland.com"

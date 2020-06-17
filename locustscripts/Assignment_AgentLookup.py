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
    def select_agentlookup(self):
        print("I am in agentlookup")
        with self.client.get("/InsuranceWebExtJS/agent_lookup.jsf", name="select_agentlookup",
                             cookies={'JSESSIONID': self.jsession_id,
                                      'UserSessionFilter.sessionId':
                                          self.userfilter_session_id},

                             catch_response=True) as self.resA3:

            if "Find an Insurance " not in self.resA3.text:
                self.resA3.failure("Got wrong response")
            else:
                self.resA3.success()
                re1 = re.findall("j_id\d+:j_id\d+", self.resA3.text)
                self.viewstate = re1[0]
                print(self.viewstate)

    @task()
    def agent_search(self):
        print("I am in agentlookup")
        with self.client.post("/InsuranceWebExtJS/agent_lookup.jsf", data={"show-all": "show-all",
                                                                           "show-all:search-all.x": "42",
                                                                           "show-all:search-all.y": "8",
                                                                           "javax.faces.ViewState": self.viewstate},
                              name="search_agent",
                              cookies={'JSESSIONID': self.jsession_id,
                                       'UserSessionFilter.sessionId':
                                           self.userfilter_session_id},
                              catch_response=True) as self.resA4:

            if "Insurance Agent Search Results" not in self.resA4.text:
                self.resA4.failure("Got wrong response")
                print(self.resA4.text)
            else:
                self.resA4.success()


class MyUser(HttpUser):
    tasks=[UserBehaviour]
    wait_time = between(2, 4)
    host = "http://demo.borland.com"
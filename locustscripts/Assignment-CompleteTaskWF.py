from locust import HttpUser, SequentialTaskSet, task,between
import uuid
import json


class UserBehaviour(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.token= ""
        self.randomid = ""
        self.request_id = ""
        self.task_id=""

    def on_start(self):
        self.token = "984970da979ab78943c0d1c74317eb1e9bd5ba7d"
        self.randomid = str(uuid.uuid4())
        resp=self.client.post("/projects", json={"name":"HelloProj2"},
                         headers={
                             "Content-Type": "application/json",
                             "X-Request-Id": self.randomid,
                             "Authorization": "Bearer " + self.token
                         },name="createproject")
        json_response_dict=json.loads(resp.text)
        print(resp.text)

        self.request_id=json_response_dict["id"]
        print("self.request_id"+str(self.request_id))


    @task()
    def createtask(self):
        print("create task")
        resp = self.client.post("/tasks",
                                json={"content": "My appointment",
                                      "due_lang": "en",
                                      "project_id": self.request_id
                                      }
                               , headers={"Content-Type": "application/json",
                                                               "Authorization": "Bearer %s" % self.token
                                                               },name="createtask")
        print(resp.text)
        json_response_dict = resp.json()

        self.task_id = json_response_dict["id"]
        print("self.task_id "+str(self.task_id ))

    @task()
    def completetask(self):
        print("complete task")

        resp = self.client.post("/tasks/" + str(self.task_id) + "/close",
                                headers={
                                    "Authorization": "Bearer %s" % self.token
                                },name="closetask")

    def on_stop(self):
        resp = self.client.delete("/projects/" + str(self.request_id),
                                  headers={
                                      "Authorization": "Bearer %s" % self.token
                                  },name="deleteproject")


class WebsiteUser(HttpUser):
    tasks = [UserBehaviour]
    host = "https://api.todoist.com/rest/v1"
    wait_time = between(5, 10)

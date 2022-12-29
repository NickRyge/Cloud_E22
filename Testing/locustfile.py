import time
import datetime
import uuid
from random import randrange
from locust import FastHttpUser, task, between

#from locust quickstart example
class QuickstartUser(FastHttpUser):
    wait_time = between(1, 5)
    
    #Locust randomly selects one of the tasks. 
    #Here there are 4, of which there are 25% chance of excercising one of them.
    @task
    def consent_main_survey(self):
        self.client.get("/consent")
        self.client.get("/main")
        self.client.get("/experiment-survey")
        
    @task
    def consent_main(self):
        self.client.get("/consent")
        self.client.get("/main")

    @task
    def consent(self):
        self.client.get("/consent")

    @task
    #Post request to the exposed google backend on port 3000 to strain the database
    def experiment(self):
        self.client.get("/consent")
        self.client.get("/main")
        self.client.get("/experiment-survey")
        self.client.post("http://34.91.192.248:3000/surveys/scale", 
        json={"userId": self.userId, "answers": [randrange(2), randrange(5), randrange(5), randrange(5)], "experimentNumber": randrange(7)})

    def on_start(self):
        self.client.get("/")
        response = self.client.post("http://34.91.192.248:3000/users/connect", json={"connectedTime": datetime.datetime.now().timestamp()})
        
        if response.status_code != 201:
            response.failure("Cant create user")
        try:
            self.userId = response.json()["userId"]
        except JSONDecodeError:
            response.failure("JSON decode error")
        except KeyError:
            response.failure("Missing userID")
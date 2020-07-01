from locust import HttpUser,SequentialTaskSet,task,between
from locust.exception import StopUser
import sys
import random
import os
import logging
import time

Root_Dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(Root_Dir)

data_folder=os.path.join(Root_Dir,"data")
file_path=os.path.join(data_folder,"credential_csv_newtour.csv")

from utilities.csvreader import CSVReader

my_reader=CSVReader(file_path).read_data()

logger=logging.getLogger(__name__)

formdata1 = {
    "tripType": "roundtrip",
    "passCount": "1",
    "fromPort": "Acapulco",
    "fromMonth": "10",
    "fromDay": "24",
    "toPort": "Acapulco",
    "toMonth": "10",
    "toDay": "24",
    "servClass": "Coach",
    "airline": "No" "Preference",
    "findFlights.x": "43",
    "findFlights.y": "11"
}
formdata2 = {
    "fromPort": "Acapulco",
    "toPort": "Acapulco",
    "passCount": "1",
    "toDay": "24",
    "toMonth": "10",
    "fromDay": "24",
    "fromMonth": "10",
    "servClass": "Coach",
    "outFlight": "Blue Skies Airlines$360$270$5:03",
    "inFlight": "Blue Skies Airlines$630$27012:23",
    "reserveFlights.x": "57",
    "reserveFlights.y": "7"
}

formdata3 = {
    "outFlightName": "Blue Skies Airlines",
    "outFlightNumber": "360",
    "outFlightPrice": "270",
    "outFlightTime": "5:03",
    "inFlightName": "Blue Skies Airlines",
    "inFlightNumber": "630",
    "inFlightPrice": "270",
    "inFlightTime": "12:23",
    "fromPort": "Acapulco",
    "toPort": "Acapulco",
    "passCount": "1",
    "toDay": "24",
    "toMonth": "10",
    "fromDay": "24",
    "fromMonth": "10",
    "servClass": "Coach",
    "subtotal": "540",
    "taxes": "44",
    "passFirst0": "qa",
    "passLast0": "mile",
    "pass.0.meal": "",
    "creditCard": "AX",
    "creditnumber": "12234567",
    "cc_exp_dt_mn": "None",
    "cc_exp_dt_yr": "None",
    "cc_frst_name": "qa",
    "cc_mid_name": "",
    "cc_last_name": "mile",
    "billAddress1": "test1,test2",
    "billAddress2": "",
    "billCity": "sss",
    "billState": "Hawaii",
    "billZip": "0000000",
    "billCountry": "215",
    "delAddress1": "1325 Borregas Ave",
    "delAddress2": "",
    "delCity": "Sunnyvale",
    "delState": "CA",
    "delZip": "94089",
    "delCountry": "215",
    "buyFlights.x": "81",
    "buyFlights.y": "10",
}


class UserBehaviour(SequentialTaskSet):

    def on_start(self):
        #Get username /pwd
        self.userName=""
        self.Password=""

        self.userName = random.choice(my_reader)['UserName']
        self.Password = random.choice(my_reader)['Password']

        with self.client.get("/", name="launchURL", catch_response=True) as resp:
            time.sleep(2)
            if resp.status_code == 200:
                resp.success()
                logger.info("URL Launched")
            else:
                resp.failure("failed to launch URL")
                logger.critical("failed to launch URL")
                #Exit test run
                self.parent.environment.runner.quit()



        with self.client.post("/login.php", name="login", data={"action": "process","userName": self.userName,
                                                           "password": self.Password,"login.x": "41","login.y": "12"}, catch_response=True) as resp:

            time.sleep(2)
            if ("Find a Flight") in resp.text:
                resp.success()
                logger.info("login successful \t" +self.userName)
            else:
                resp.failure("failed to login")
                logger.critical("login failed \t" +self.userName)
                #Exit User
                raise StopUser()

    @task()
    def find_flight(self):

        #Select a Flight
        with self.client.post("/mercuryreservation2.php", data=formdata1,name="Find_Flight",catch_response=True) as res_1:
            time.sleep(2)
            if("Select a Flight") in res_1.text:
                res_1.success()
                logger.info("find flight successful \t" + self.userName)
            else:
                res_1.failure("find flight failed"+res_1.text)
                logger.error("find flight failed \t" + self.userName)


    @task()
    def select_flight(self):

        #Book a Flight
        with self.client.post("/mercurypurchase.php", data=formdata2,name="Select_Flight",catch_response=True) as res_2:
            time.sleep(2)
            if("Book a Flight") in res_2.text:

                res_2.success()
                logger.info("Select a Flight successful \t" + self.userName)
            else:
                res_2.failure("select flight failed"+res_2.text)
                logger.error("Select a Flight failed \t" + self.userName)

    @task()
    def book_flight(self):

        #Flight Confirmation
        with self.client.post("/mercurypurchase2.php", data=formdata3,name="Book_Flight",catch_response=True) as res_3:
            time.sleep(2)
            if("Flight Confirmation") in res_3.text:
                res_3.success()
                logger.info("Book a Flight successful \t" + self.userName)
            else:
                res_3.failure("book flight failed"+res_3.text)
                logger.error("Book a Flight failed \t" + self.userName)

class MyUser(HttpUser):
    wait_time=between(1,2)
    # host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]

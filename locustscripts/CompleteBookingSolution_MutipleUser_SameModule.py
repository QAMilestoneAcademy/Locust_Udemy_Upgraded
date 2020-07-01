from locust import HttpUser,SequentialTaskSet,task,between

UserName = [
        ("qamile1@gmail.com", "qamile"),
        ("qamile2@gmail.com", "qamile"),
        ("qamile3@gmail.com", "qamile"),
        ("qamile4@gmail.com", "qamile"),
        ("qamile5@gmail.com", "qamile")
    ]
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
        if(len(UserName)>0):
            self.userName, self.Password= UserName.pop()
            print(self.userName, self.Password)
            UserName.insert(0,(self.userName, self.Password))
            print(UserName)
        else:
            print("User List is empty")

        with self.client.post("/login.php", name="login", data={"action": "process","userName": self.userName,
                                                           "password": self.Password,"login.x": "41","login.y": "12"}, catch_response=True) as resp:

            if ("Find a Flight") in resp.text:
                resp.success()
            else:
                resp.failure("failed to login")
    @task()
    def find_flight(self):
        print("add post request to search flight")
        print("verify with catch response that flight search is successful")
        #Select a Flight
        with self.client.post("/mercuryreservation2.php", data=formdata1,name="Find_Flight",catch_response=True) as res_1:
            if("Select a Flight") in res_1.text:
                res_1.success()
            else:
                res_1.failure("find flight failed"+res_1.text)


    @task()
    def select_flight(self):
        print("add post request to select flight")
        print("verify with catch response that select flight is successful")
        #Book a Flight
        with self.client.post("/mercurypurchase.php", data=formdata2,name="Select_Flight",catch_response=True) as res_2:
            if("Book a Flight") in res_2.text:
                res_2.success()
            else:
                res_2.failure("select flight failed"+res_2.text)

    @task()
    def book_flight(self):
        print("add post request to book flight")
        print("verify with catch response that flight book is successful")
        print("once success criteria is met, you can change criteria to wrong wordings to see fail criteria is working")
        #Flight Confirmation
        with self.client.post("/mercurypurchase2.php", data=formdata3,name="Book_Flight",catch_response=True) as res_3:
            if("Flight Confirmation") in res_3.text:
                res_3.success()
            else:
                res_3.failure("book flight failed"+res_3.text)

class MyUser(HttpUser):
    wait_time=between(1,2)
    host="http://newtours.demoaut.com"
    tasks=[UserBehaviour]

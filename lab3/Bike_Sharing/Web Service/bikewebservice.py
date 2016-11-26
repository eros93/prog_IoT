
import json
import requests
from operator import itemgetter

class BikeWebService():

    exposed = True

    def __init__(self, id):
        self.id = id


    def Get_Json(self):
        r=requests.get("https://www.bicing.cat/availability_map/getJsonObject")
        self.data = json.loads(r.text)
        return self.data


    def search_more_Slot(self, N="10", string="desc"):
        
        if (N.isdigit()):
            N=int(float(N))
            if (string=="asc")|(string=="ascending")|(string=="desc")|(string=="descending"):
                if((string=="asc")|(string=="ascending")):
                    rev = False
                else:
                    rev = True

                self.Get_Json()
                if (int(float(N)) <= len(self.data)) & (int(float(N)) >= 0):
                    ordered_list = sorted(self.data, key=itemgetter("slots"), reverse=rev)
                    self.data = ordered_list
                    self.result=[]
                    for x in range(N):
                        self.result.append(self.data[x])
                else:
                    raise NameError("\n\tN must be lower than %d" %len(self.data))

            else:
                raise NameError("\n\tNot valid Input! Try again")
        else:
            raise NameError ("\n\tN must be a number!!! (integer)")


    def search_more_Bike(self, N="10", string="desc"):
        
        if (N.isdigit()):
            N=int(float(N))
            if (string=="asc")|(string=="ascending")|(string=="desc")|(string=="descending"):
                if((string=="asc")|(string=="ascending")):
                    rev = False
                else:
                    rev = True

                self.Get_Json()
                if (int(float(N)) <= len(self.data)) & (int(float(N)) >= 0):
                    ordered_list = sorted(self.data, key=itemgetter("bikes"), reverse=rev)
                    self.data = ordered_list
                    self.result=[]
                    for x in range(N):
                        self.result.append(self.data[x])
                else:
                    raise NameError("\n\tN must be lower than %d" %len(self.data))

            else:
                raise NameError("\n\tNot valid Input! Try again")
        else:
            raise NameError ("\n\tN must be a number!!! (integer)")


    def all_station_Zip(self, zip_code):

        self.Get_Json()
        self.result=[]
        for x in range(len(self.data)):
            if self.data[x]["zip"] == zip_code:
                self.result.append(self.data[x])


    def search_more_Bikes(self, N="10"):

        if N.isdigit():
            N=int(float(N))

            self.Get_Json()
            self.result=[]
            for x in range(len(self.data)):
                if self.data[x]["stationType"] == "ELECTRIC_BIKE":
                    if int(float(self.data[x]["bikes"])) > N:
                        self.result.append(self.data[x])

        else:
            raise NameError ("\n\tN must be a number!!! (integer)")


    def all_bikes_slots_district(self, district):

        self.Get_Json()
        tot_bikes=0
        tot_slots=0
        for x in range(len(self.data)):
            if self.data[x]["district"] == district:
                tot_slots = tot_slots + int(float(self.data[x]["slots"]))
                tot_bikes = tot_bikes + int(float(self.data[x]["bikes"]))
        self.result={}
        self.result["tot_slots"] = tot_slots
        self.result["tot_bikes"] = tot_bikes


    def GET(self, *uri, **params):
        if params["idcommand"]=="1":
            self.search_more_Slot(params["N"], params["order"])
            return json.dumps(self.result)

        elif params["idcommand"]=="2":
            self.search_more_Bike(params["N"], params["order"])
            return json.dumps(self.result)

        elif params["idcommand"]=="3": 
            self.all_station_Zip(params["zipcode"])
            return json.dumps(self.result)
        
        elif params["idcommand"]=="4":
            self.search_more_Bikes(params["N"])
            return json.dumps(self.result)

        elif params["idcommand"]=="5":
            self.all_bikes_slots_district(params["district"])
            return json.dumps(self.result)

        else:
            raise NameError ("\n\t Not a valid IDcommand!")
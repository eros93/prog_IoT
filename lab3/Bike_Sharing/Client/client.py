#CLIENT for Barcelona BIKE SHARING info

from tools import Tools
import requests
import json

print ("\n\n\t----------> Bike Sharing Barcelona Client <----------")
print ("\n\t------------> Powered by E&E <-------------")
print("\n\t    (Working with Web Service by E&E)")

ans=True
while ans:
    print("""
    MENU:
    1. Show first N stations with more SLOTS available
    2. Show first N stations with more BIKES available
    3. Get all stations of a ZIP
    4. Get all stations with more than N Electric BIKE
    5. Count all available BIKES and SLOTS in a DISTRICT
    6. Exit
    """)

    ans=raw_input("\n\n\tWhat would you like to do?\t")
    tool = Tools(1)
    url_req='http://localhost:8080/'

    if ans=="1": 
        print("\n\t---> Show first N stations with more SLOTS available (default N=10, order=descending)")
        N = raw_input("\n\n\tHow many stations to display? (N)\t")
        order = raw_input("\n\n\tIn which order? (<ascending> or <descending>):\t").lower()
        parameters={"idcommand":ans,"N":N, "order":order}
        
        print("\n\tContacting E&E Barcelona Bike Sharing web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            print("\n\tHere is the result:")
            result=json.loads(r.text)
            for x in range(len(result)):
                tool.Display_station(result[x])
            tool.print_logo()
        else: print("\n\tBad Response from Web Server")

    elif ans=="2":
        print("\n\t---> Show first N stations with more BIKES available (default N=10, order=descending)")
        N = raw_input("\n\n\tHow many stations to diplay? (N)\t")
        order = raw_input("\n\n\tIn which order? (<ascending> or <descending>):\t").lower()
        parameters={"idcommand":ans,"N":N, "order":order}
        
        print("\n\tContacting E&E Barcelona Bike Sharing web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            print("\n\tHere is the result:")
            result=json.loads(r.text)
            for x in range(len(result)):
                tool.Display_station(result[x])
            tool.print_logo()
        else: print("\n\tBad Response from Web Server")
    
    elif ans=="3": 
        print("\n\t---> Get all the stations of a given ZIP code")
        zip_code = raw_input("\n\n\tWhich ZIP?\t")
        parameters={"idcommand":ans,"zipcode":zip_code}
        
        print("\n\tContacting E&E Barcelona Bike Sharing web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            print("\n\tHere is the result:")
            result=json.loads(r.text)
            for x in range(len(result)):
                tool.Display_station(result[x])
            tool.print_logo()
        else: print("\n\tBad Response from Web Server")
    
    elif ans=="4":
        print("\n\t---> Get all stations with at least N ELECTRIC BIKES")
        N = raw_input("\n\n\tSet the minimum number of electric bikes (N):\t")
        parameters={"idcommand":ans,"N":N}
        
        print("\n\tContacting E&E Barcelona Bike Sharing web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            print("\n\tHere is the result:")
            result=json.loads(r.text)
            for x in range(len(result)):
                tool.Display_station(result[x])
            tool.print_logo()
        else: print("\n\tBad Response from Web Server")

    elif ans=="5":
        print("\n\t---> Count all available BIKES and SLOTS in a DISTRICT")
        district = raw_input("\n\n\tWhich DISTRICT?\t")
        parameters={"idcommand":ans,"district":district}
        
        print("\n\tContacting E&E Barcelona Bike Sharing web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            print("\n\tHere is the result:")
            result=json.loads(r.text)
            print("\n\tTotal Bikes: %d" %result["tot_bikes"])
            print("\n\tTotal Slots: %d" %result["tot_slots"])
        else: print("\n\tBad Response from Web Server")
    
    elif ans=="6": 
        print("\n\t---> Exiting....\n")
        ans=False

    elif ans !="": 
        print("\n\tNot Valid Choice Try again")
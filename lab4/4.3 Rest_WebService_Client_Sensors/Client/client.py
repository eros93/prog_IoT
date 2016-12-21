import requests
import json

ip_webservice = "192.168.1.254"
port_webservice = "8080"

print ("\n\n\t----------> Sensor&Relay Service Client <----------")
print ("\n\t------------> Powered by E&E <-------------")
print("\n\t    (Working with Web Service by E&E)")

#ip_webservice = raw_input("\n\tIP of the Web Service: ")
#port_webservice = raw_input("\tAt Port: ")
url_req='http://'+ip_webservice+':'+port_webservice+'/'

ans=True
while ans:
    print("""
    MENU:
    1. Get TEMPERATURE from sensor
    2. Get HUMIDITY from sensor
    3. Get both TEMPERATURE and HUMIDITY
    4. Get the STATUS of RELAY
    5. CHANGE status of RELAY
    6. Exit
    """)

    ans=raw_input("\n\n\tWhat would you like to do?\t")
    if ans=="1":
        print("\n\t---> Get TEMPERATURE")
        r=requests.get(url_req+"temp")
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            result=json.loads(r.text)
            print("\n\tTemperature: "+result["temp"]+"*C")
        else: print("\n\tBad Response from Web Server")

    elif ans=="2":
        print("\n\t---> Get HUMIDITY")
        r=requests.get(url_req+"hum")
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            result=json.loads(r.text)
            print("\n\tHumidity: "+result["hum"]+"%")
        else: print("\n\tBad Response from Web Server")

    elif ans=="3":
        print("\n\t---> Get TEMPERATURE and HUMIDITY")
        r=requests.get(url_req+"all")
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            result=json.loads(r.text)
            print("\n\tTemperature: "+result["temp"]+"*C")
            print("\tHumidity: "+result["hum"]+"%")
        else: print("\n\tBad Response from Web Server")

    elif ans=="4":
        print("\n\t---> Get RELAY STATUS (0-->OFF and 1-->ON)")
        r=requests.get(url_req+"relay_stat")
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            result=json.loads(r.text)
            print("\n\tRelay status: "+result["relay_stat"])
        else: print("\n\tBad Response from Web Server")

    elif ans=="5":
        print("\n\t---> CHANGE status of RELAY")
        stat = raw_input("\n\tNew relay status (0-->OFF and 1-->ON): ")
        parameters={"stat":stat}
        r=requests.get(url_req+"relay_set", params=parameters)
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            result=json.loads(r.text)
            print("\n\tRelay Status is changed! New status: "+result["relay_stat"])
        else: print("\n\tBad Response from Web Server")

    elif ans=="6":
        print("\n\t---> Exiting....\n")
        ans=False

    elif ans=="":
        print("\n\tNot Valid Choice Try again")
#Program to managing a Discography contactin the web service!!!

import json
import requests


print ("\n\n\t----------> WEBDISCOGRAPHY MANAGER <----------")
print ("\n\t------------> Powered by E&E <-------------")
print ("\n\t(Remotely working on 'discography.json')")

ans=True
while ans:
    print("""
    MENU:
    1. Search by Artist
    2. Search by Title
    3. Search by Pubblication Year
    4. Search by Total Tracks
    5. Insert New Disc
    6. See All the Discography
    7. Delete a Disc
    8. Exit
    """)

    ans=raw_input("\n\n\tWhat would you like to do?\t")
    
    if ans=="1": 
        print("\n\t---> Search by Artist\n")
        input_string=raw_input("\n\tPlease insert <artist_name>: ")
        
        url_req='http://localhost:8080/'
        body={'idcommand':ans,'key_word':input_string}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.post(url_req, data=json.dumps(body))
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            try:
                payload=json.loads(r.text)
                print "\n\tResult:\n"
                print payload['found_list']
                print "\n"
            except:
                print "\n\t--> Artist Not Found\n"
        else: print("\n\tBad Response from Web Server")

    elif ans=="2": 
        print("\n\t---> Search by Title\n")
        input_string=raw_input("\n\tPlease insert <title>: ")
        
        url_req='http://localhost:8080/'
        body={'idcommand':ans,'key_word':input_string}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.post(url_req, data=json.dumps(body))
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            try:
                payload=json.loads(r.text)
                print "\n\tResult:\n"
                print payload['found_list']
                print "\n"
            except:
                print "\n\t--> Title Not Found\n"
        else: print("\n\tBad Response from Web Server")

    elif ans=="3": 
        print("\n\t---> Search by Year\n")
        input_string=raw_input("\n\tPlease insert <year>: ")
        
        url_req='http://localhost:8080/'
        body={'idcommand':ans,'key_word':input_string}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.post(url_req, data=json.dumps(body))
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            try:
                payload=json.loads(r.text)
                print "\n\tResult:\n"
                print payload['found_list']
                print "\n"
            except:
                print "\n\t--> Pubblication Year Not Found\n"
        else: print("\n\tBad Response from Web Server")
    
    elif ans=="4": 
        print("\n\t---> Search by Total Tracks\n")
        input_string=raw_input("\n\tPlease insert <total_tracks>: ")
        
        url_req='http://localhost:8080/'
        body={'idcommand':ans,'key_word':input_string}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.post(url_req, data=json.dumps(body))
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            try:
                payload=json.loads(r.text)
                print "\n\tResult:\n"
                print payload['found_list']
                print "\n"
            except:
                print "\n\t--> Total Tracks Not Found\n"
        else: print("\n\tBad Response from Web Server")

    elif ans=="5": 
        input_string={}
        print("\n\t---> Insert New Disc\n")
        input_string["artist"]=raw_input("\n\tPlease insert <artist_name>: ")
        input_string["title"]=raw_input("\n\tPlease insert <title>: ")
        input_string["publication_year"]=eval(raw_input("\n\tPlease insert <publication_year>: "))
        input_string["total_tracks"]=eval(raw_input("\n\tPlease insert <total_tracks>: "))

        url_req='http://localhost:8080/'
        body={'idcommand':ans,'new_album':input_string}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.put(url_req, data=json.dumps(body))
        if r.status_code==200:
            print("\t--> REQUEST SUCCESS!")
            payload=json.loads(r.text)
            print "\n\tResult:\n"
            if payload['response'] ==0 :
                print "\n\t--> Album inserted"
            else:
                print "\t -->",payload['response']
            print "\n"
        else: print("\n\tBad Response from Web Server")
        
        print("\n\t---> Save changes and exiting....\n")
        ans=False

    elif ans=="6": 
        print("\n\t---> See all discography 'discography.json'\n")
        
        url_req='http://localhost:8080/'
        parameters={'idcommand':ans}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.get(url_req, params=parameters)
        if r.status_code==200:
            payload=json.loads(r.text)
            print("\t--> REQUEST SUCCESS!")
            print "\n\tResult:\n"
            print payload
            print "\n"
        else: print("\n\tBad Response from Web Server")

    elif ans=="7":
        print("\n\t---> Delete a Disc'\n")
        artist=raw_input("\n\tPlease insert <artist_name>: ")
        title=raw_input("\n\tPlease insert <title>: ")
        
        url_req='http://localhost:8080/'
        parameters={'idcommand':ans, 'artist':artist, 'title':title}
        print("\n\tContacting DISCOGRAPHY web service...")
        r=requests.delete(url_req, params=parameters)
        if r.status_code==200:
            payload=json.loads(r.text)
            print("\t--> REQUEST SUCCESS!")
            print "\n\tResult:\n"
            if payload['response'] == 0 :
                print "\n\t--> Album deleted"
            else:
                print "\t -->",payload['response']
            print "\n"
        else: print("\n\tBad Response from Web Server")

    elif ans=="8": 
        print("\n\t---> Exiting....\n")
        ans=False

    elif ans !="": 
        print("\n\tNot Valid Choice Try again")
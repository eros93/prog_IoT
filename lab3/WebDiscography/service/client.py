#Program to managing a Discography
# -----> python main.py [filename_discography.json]

from discography import Discography
#import json


print ("\n\n\t----------> DISCOGRAPHY MANAGER <----------")
print ("\n\t------------> Powered by E&E <-------------")

filename = raw_input("\n\tPlease insert the name of JSON file containing the discography: ")
if filename == "":
	filename = "discography.json"
disc = Discography(filename)

ans=True
while ans:
    print("""
	1. Search by Artist
	2. Search by Title
	3. Search by Pubblication Year
	4. Search by Total Tracks
	5. Insert New Disc
	6. See All the Discography
	7. Exit
	""")
	
    ans=raw_input("\n\n\tWhat would you like to do?\t")
    if ans=="1": 
        print("\n\t---> Search by Artist\n")
        input_string=raw_input("\n\tPlease insert <artist_name>: ")
        disc.search_by_artist(input_string)

    elif ans=="2": 
        print("\n\t---> Search by Title\n")
        input_string=raw_input("\n\tPlease insert <title>: ")
        disc.search_by_title(input_string)

    elif ans=="3": 
        print("\n\t---> Search by Year\n")
        input_string=raw_input("\n\tPlease insert <year>: ")
        disc.search_by_pubblication_year(input_string)

    elif ans=="4": 
        print("\n\t---> Search by Total Tracks\n")
        input_string=raw_input("\n\tPlease insert <total_tracks>: ")
        disc.search_by_total_tracks(input_string)

    elif ans=="5": 
    	input_string={}
        print("\n\t---> Insert New Disc\n")
        input_string["artist"]=raw_input("\n\tPlease insert <artist_name>: ")
        input_string["title"]=raw_input("\n\tPlease insert <title>: ")
        input_string["publication_year"]=eval(raw_input("\n\tPlease insert <publication_year>: "))
        input_string["total_tracks"]=eval(raw_input("\n\tPlease insert <total_tracks>: "))
        disc.insert_new_album(input_string)
        print("\n\t---> Save changes and exiting....\n")
        ans=False

    elif ans=="6": 
        print("\n\t---> See all discography "+filename+" \n")
        disc.print_all()

    elif ans=="7": 
        print("\n\t---> Exiting....\n")
        ans=False

    elif ans !="": 
        print("\n\tNot Valid Choice Try again")
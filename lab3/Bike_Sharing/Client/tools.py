
class Tools:

    def __init__(self, id):
        self.id = id

    def Display_station(self,input_list):
        print "\n\tID: %s" %input_list["id"]
        print "\n\tName: %s" %input_list["name"]
        try:
            print "\n\tAddress: %s n.%s" %(input_list["address"],input_list["addressNumber"])
        except:
            print "\n\tAddress: %s" %input_list["address"]
        print "\n\tDistrict: %s" %input_list["district"]
        print "\n\tZip: %s" %input_list["zip"]

        print "\n\n\tLongitude: %s" %input_list["lon"]
        print "\n\tLatitude: %s" %input_list["lat"]
        
        print "\n\n\tBikes: %s" %input_list["bikes"]
        print "\n\tSlots: %s" %input_list["slots"]
        print "\n\tType: %s" %input_list["stationType"]

        print "\n\n\tStatus: %s" %input_list["status"]
        print "\n\tNearby stations: %s" %input_list["nearbyStations"]
        print "\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        return

    def print_logo(self):
        print """
        -------- __@      __@       __@       __@      __~@
        ----- _`\<,_    _`\<,_    _`\<,_     _`\<,_    _`\<,_
        ---- (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
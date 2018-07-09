import os
if os.system("ping -c 1 192.168.1.7") == 0:
 print "up"

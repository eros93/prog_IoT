from withdraw import Withdraw, MyPublisher
import json
import urllib2
import time
import schedule
from datetime import datetime

RESOURCECAT_IP = "192.168.1.71"
RESOURCECAT_PORT = 8080

myWithdraw = Withdraw("WithDraw1")

def periodic_withdraw_control():
	print ("Periodic_withdraw_control started at %s" %time.strftime("%H:%M"))
	all_res_cat = myWithdraw.get_all_data(RESOURCECAT_IP, RESOURCECAT_PORT)
	myWithdraw.search_topic_inpump(all_res_cat)
	myWithdraw.run()
	if myWithdraw.stop_flag:
		print "Withdraw Control ended."


if  __name__ == "__main__":

	#periodic_withdraw_control()	#DEBUG

	schedule.every().day.at("01:00").do(periodic_withdraw_control)
	
	while True:
		schedule.run_pending()
		time.sleep(1)
from withdraw import Withdraw, MyPublisher
import json
import urllib2
import time
import schedule
from datetime import datetime

RESOURCECAT_IP = "192.168.1.71"
RESOURCECAT_PORT = 8080


def periodic_withdraw_control():
	myWithdraw=Withdraw("WithDraw1")
	all_res_cat = myWithdraw.get_all_data(RESOURCECAT_IP, RESOURCECAT_PORT)
	myWithdraw.search_topic_inpump(all_res_cat)
	myWithdraw.run()


if  __name__ == "__main__":

	#periodic_withdraw_control()

	schedule.every().day.at("01:00").do(periodic_withdraw_control(myWithdraw))
	
	while True:
		schedule.run_pending()
		time.sleep(1)

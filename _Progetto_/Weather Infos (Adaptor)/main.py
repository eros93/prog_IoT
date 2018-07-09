#Web service for elaboration of data from the DARK SKY API

import requests
import json
from weatheradaptor import ResourceCatalog, WeatherInfo, MyPublisher
import time
import schedule
from datetime import datetime

#Resource Catalog
IP_resource_catalog = "192.168.1.73"
port_resource_catalog = 8080


def build_packet(json_pkt, prob_th, int_th):
	tmp_pkt = json.loads(json_pkt)
	
	#Set the system on "OFF"
	tmp_pkt["watering_flag"] = "False"

	if ( (tmp_pkt["precipProb"] <= prob_th) & (tmp_pkt["precipInt"] <= int_th) ):
		tmp_pkt["watering_flag"] = "True"	#if it will NOT raining ==> Set	system on "ON"

	return json.dumps(tmp_pkt)

def periodical_update():

	print datetime.today()

	#Retrieve infos from Resource Catalog
	res_cat = ResourceCatalog(IP_resource_catalog, port_resource_catalog)

	#Retrieve forecast from Weather API
	w_info = WeatherInfo(res_cat.api_key, res_cat.lat, res_cat.lng)

	#Build the final JSON (also WITHDRAW/WATERING DECISION)
	packet = build_packet(w_info.tomorrow_forecast(), res_cat.probprec_th, res_cat.intprec_th)

	#Mqtt publisher on given topic
	mqtt_pub = MyPublisher("weath_adpt")
	mqtt_pub.start(res_cat.broker_ip, res_cat.broker_port)
	mqtt_pub.myPublish(res_cat.mqtt_t_out, packet, 2, True)
	mqtt_pub.stop()

	return


if __name__ == "__main__":

	periodical_update()		# DEBUG

	schedule.every().day.at("21:00").do(periodical_update)

	while True:
		schedule.run_pending()
		time.sleep(60)
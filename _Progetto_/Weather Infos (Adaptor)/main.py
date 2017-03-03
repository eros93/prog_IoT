#Web service for elaboration of data from the DARK SKY API

import requests
from weatheradaptor import ResourceCatalog, WeatherInfo, MyPublisher
import time
import schedule
from datetime import datetime

#Resource Catalog
IP_resource_catalog = "192.168.1.70"
port_resource_catalog = 8080


def periodical_update():

	print datetime.today()

	#Retrieve infos from Resource Catalog
	res_cat = ResourceCatalog(IP_resource_catalog, port_resource_catalog)

	#Retrieve forecast from Weather API
	w_info = WeatherInfo(res_cat.api_key, res_cat.lat, res_cat.lng)

	#Mqtt publisher on given topic
	mqtt_pub = MyPublisher("weath_adpt")
	mqtt_pub.start(res_cat.broker_ip, res_cat.broker_port)
	mqtt_pub.myPublish(res_cat.mqtt_t_out, w_info.tomorrow_forecast(), 2, True)
	mqtt_pub.stop()

	return


if __name__ == "__main__":

	periodical_update()

	schedule.every().day.at("21:00").do(periodical_update)

	while True:
		schedule.run_pending()
		time.sleep(10)
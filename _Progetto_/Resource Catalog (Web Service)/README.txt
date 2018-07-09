README file

To start the web service --> run "main.py"!

Brief summary of RESTful API of Resource Catalog


GET request:
	
	- All the resource catalog: GET localhost:8080/res_cat/all
	--> return JSON of Resource Catalog

	- Broker info (Ip and Port): GET localhost:8080/res_cat/broker_info
	--> return JSON string
		{"broker_ip": "x.x.x.x", "request": "broker_info", "broker_port": "x", "timestamp":00000000000}
		N.B. Timestamp is used only by Arduino to retrieve the time!
	
	- Vector of devices: GET localhost:8080/res_cat/dev_list
	--> return the updated vector in JSON containg the registered devices
		[{"ip_address": "x.x.x.x", "rn": "...", "mqtt_topic": "...", "resources": ["...", "..."]}, ...]

	- Informations useful for weather adaptor: GET localhost:8080/res_cat/weather_adaptor
	--> return JSON string
		{"latitude": x, "api_key": "...", "probprec_th": x, "intprec_th": x, "request": "loc_info", "longitude": x, "mqtt_t_out":"...", }

	- Informations about thresholds : #GET localhost:8080/res_cat/thresholds
	--> return JSON string
		{"usedwater_topic": "...", "probprec_th": x, "request": "thresholds", "intprec_th": x}


POST request:
	
	- Register/insert a new device: POST localhost:8080/res_cat/new_dev 
									with Body --> JSON {"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}
	--> return the updated VECTOR in JSON containg the registered devices
		[{"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}, ...]


PUT request:
	
	- Update the infos of a specific device: PUT localhost:8080/res_cat/upd_dev_res
											with body --> JSON {"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], 							"subnet":"...", "mqtt_role":"..."}
	--> return the updated info of the related device into a JSON 
		{"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}


DELETE request:

	- Remove/delete a device given its resource name <rn>: DELETE localhost:8080/res_cat/del_dev?rn=...
	--> return the updated vector in JSON containg the remaining registered devices
		[{"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}, ...]



OBSERVATION
- <resource_name> need to be unique? I think so...
- Eventual extra infos given through POST and PUT request are not used/stored. (If it is necessary --> need to change the source code! --> Contact Enrico!)


STRUCTURE OF DEVICE INFOs
{
	"rn": <resource name>,

	"ip_address": "x.x.x.x",
	
	"subnet": "1",	--> refers to which plants row (for the actuators is un-necessary?)
	
	"mqtt_role": "p",	--> p <publisher>, s <subscriber>, c <client> (both sub&pub)

	"mqtt_topic": "sensor/subnet/1/hum_temp",
	
	"resources": ["temp", "hum_gr"]	--> refers to the respurces this device exposes
}
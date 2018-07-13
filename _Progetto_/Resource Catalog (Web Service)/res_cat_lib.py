#!/usr/bin/python

import json
import cherrypy
import time

class ResourceCatalog(object):
	
	exposed = True

	def __init__(self, id):
		self.id = id
		self.obj_tmp={}

	def read_rc(self):
		self.rc = open("./resource_catalog.json", "r")
		self.rc_all = self.rc.read()
		self.rc.close()
		self.rc_obj = json.loads(self.rc_all)
		self.broker_ip = self.rc_obj["broker_ip"]
		self.broker_port = self.rc_obj["broker_port"]
		self.dev_list = self.rc_obj["dev_list"]
		self.weath_api_key = self.rc_obj["weath_api_key"]
		self.lat = self.rc_obj["latitude"]
		self.lng = self.rc_obj["longitude"]
		self.weath_adpt_out_topic = self.rc_obj["weath_mqtt_out_topic"]
		self.probprec_th = self.rc_obj["precipprobability_thresh"]
		self.intprec_th = self.rc_obj["precipintensity_thresh"]
		self.usedwater_topic = self.rc_obj["usedwater_topic"]
		self.usedwater_topic_bot = self.rc_obj["usedwater_topic_bot"]
		self.watertemp_th = self.rc_obj["watertemp_thresh"]
		self.moisture_th = self.rc_obj["moisture_thresh"]
		#continue here for other elements!!!
		return

	def insert_new_dev(self, rn, ip_add, mqtt_t, res, subn, mqtt_r):
		self.read_rc()
		for x in self.dev_list:
			if (x["rn"]!=rn)and(x["ip_address"]!=ip_add):
				continue
			else:
				raise NameError("It is not possible to insert a new device with same <resource_name> and <IP> of an existing one!")

		obj={}
		obj["rn"] = rn
		obj["ip_address"] = ip_add
		obj["mqtt_topic"] = mqtt_t
		obj["resources"] = res
		obj["subnet"] = subn
		obj["mqtt_role"] = mqtt_r
		self.read_rc()
		self.rc_obj["dev_list"].append(obj)
		self.rc = open("./resource_catalog.json", "w")
		self.rc.truncate()
		self.rc.write(json.dumps(self.rc_obj, sort_keys=True, indent=4, separators=(',', ': ')))
		self.rc.close()
		self.read_rc()
		return json.dumps(self.dev_list)
    	
	def delete_dev(self, rn):
		self.read_rc()

		hit = None
		for x in range(len(self.dev_list)):
			if self.dev_list[x]["rn"]==rn:
				hit=x
				break
			else:
				continue
		if hit!=None:
			del self.rc_obj["dev_list"][hit]
			self.rc = open("./resource_catalog.json", "w")
			self.rc.truncate()
			self.rc.write(json.dumps(self.rc_obj, sort_keys=True, indent=4, separators=(',', ': ')))
			self.rc.close()
			self.read_rc()
			return json.dumps(self.dev_list)
		else:
			raise NameError("There is no device with the given <resource_name>/<IP> !")

	def update_dev_resources(self, rn, ip_add, mqtt_t, res, subn, mqtt_r):
		self.delete_dev(rn)
		self.insert_new_dev(rn, ip_add, mqtt_t, res, subn, mqtt_r)
		self.read_rc()
		for x in range(len(self.dev_list)):
			if self.dev_list[x]["rn"]==rn:
				return json.dumps(self.dev_list[x])
			else:
				continue
		raise NameError("Something wrong during UPDATING the device infos!")

	def update_thresholds(self, threshold, value):
		self.read_rc()
		rc = open("./resource_catalog.json", "r")
		rc_all = rc.read()
		rc.close()
		rc_obj = json.loads(rc_all)

		if(rc_obj.has_key(threshold)):
			rc_obj[threshold] = float(value)
			rc = open("./resource_catalog.json", "w")
			rc.truncate()
			rc.write(json.dumps(rc_obj, sort_keys=True, indent=4, separators=(',', ': ')))
			rc.close()
			self.read_rc()
			return True
		else:
			return False
			
	
	def GET(self, *uri, **params):
		
		#GET localhost:8080/res_cat/all
		if uri[0]=="all":
			self.read_rc()
			return self.rc_all

		#GET localhost:8080/res_cat/broker_info
		elif uri[0]=="broker_info":
			self.read_rc()
			self.obj_tmp = {}
			self.obj_tmp["broker_ip"] = self.broker_ip
			self.obj_tmp["broker_port"] = self.broker_port
			self.obj_tmp["request"] = uri[0]
			self.obj_tmp["timestamp"] = int(time.time())
			return json.dumps(self.obj_tmp)

		#GET localhost:8080/res_cat/dev_list
		elif uri[0]=="dev_list":
			self.read_rc()
			return json.dumps(self.dev_list)

		#GET localhost:8080/res_cat/weather_adaptor
		elif uri[0]=="weather_adaptor":
			self.read_rc()
			self.obj_tmp = {}
			self.obj_tmp["request"] = uri[0]
			self.obj_tmp["api_key"] = self.weath_api_key
			self.obj_tmp["latitude"] = self.lat
			self.obj_tmp["longitude"] = self.lng
			self.obj_tmp["mqtt_t_out"] = self.weath_adpt_out_topic
			self.obj_tmp["probprec_th"] = self.probprec_th
			self.obj_tmp["intprec_th"] = self.intprec_th
			return json.dumps(self.obj_tmp)

		#GET localhost:8080/res_cat/thresholds
		elif uri[0]=="thresholds":
			self.read_rc()
			self.obj_tmp = {}
			self.obj_tmp["request"] = uri[0]
			self.obj_tmp["usedwater_topic"] = self.usedwater_topic
			self.obj_tmp["usedwater_topic_bot"] = self.usedwater_topic_bot
			self.obj_tmp["moisture_th"] = self.moisture_th
			self.obj_tmp["watertemp_th"] = self.watertemp_th
			self.obj_tmp["probprec_th"] = self.probprec_th
			self.obj_tmp["intprec_th"] = self.intprec_th
			return json.dumps(self.obj_tmp)


		else:
			raise NameError("Not a valid URI command!")


	def POST(self, *uri, **params):

		#POST localhost:8080/res_cat/new_dev
		#Body --> JSON {"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}
		if uri[0]=="new_dev":
			json_input = cherrypy.request.body.read()
			obj = json.loads(json_input)

			if (obj.has_key("rn"))and(obj.has_key("ip_address"))and(obj.has_key("mqtt_topic"))and(obj.has_key("resources"))and(obj.has_key("subnet"))and(obj.has_key("mqtt_role")):
				return self.insert_new_dev(obj["rn"],obj["ip_address"],obj["mqtt_topic"],obj["resources"],obj["subnet"],obj["mqtt_role"])
			else:
				raise NameError("Json structure of input data is not correct!")

		else:
			raise NameError("Not a valid URI command!")


	def PUT(self,*uri,**params):

		#PUT localhost:8080/res_cat/upd_dev_res
		#Body --> JSON {"rn":"...", "ip_address": "x.x.x.x", "mqtt_topic":"...", "resources": ["...","..."], "subnet":"...", "mqtt_role":"..."}
		if uri[0]=="upd_dev_res":
			json_input = cherrypy.request.body.read()
			obj = json.loads(json_input)

			if (obj.has_key("rn"))and(obj.has_key("ip_address"))and(obj.has_key("mqtt_topic"))and(obj.has_key("resources"))and(obj.has_key("subnet"))and(obj.has_key("mqtt_role")):
				return self.update_dev_resources(obj["rn"],obj["ip_address"],obj["mqtt_topic"],obj["resources"],obj["subnet"],obj["mqtt_role"])
			raise NameError("Json structure of input data is not correct!")
		
		#PUT localhost:8080/res_cat/upd_thresholds
		#Body --> JSON { "moisture" : float, "watertemp" : float, "precipint" : float, "precipprob" : float }
		#must be 'application/json' !!!
		elif uri[0]=="upd_thresholds":
			json_input = cherrypy.request.body.read()
			obj = json.loads(json_input)
			
			tmp_params = {}
			if (obj.has_key("moisture")):
				tmp_params["moisture_thresh"] = obj["moisture"]

			if(obj.has_key("watertemp")):
				tmp_params["watertemp_thresh"] = obj["watertemp"]

			if(obj.has_key("precipint")):
				tmp_params["precipintensity_thresh"] = obj["precipint"]
						
			if(obj.has_key("precipprob")):
				tmp_params["precipprobability_thresh"] = obj["precipprob"]
			
			# check if almost one obj element was correct
			if tmp_params:
				# for each parameter correct, execute the update
				for key in tmp_params:
					if(self.update_thresholds(key,tmp_params[key])):
						print("Updating %s OK!" %(key))
					else:
						print("Updating %s FAILED!" %(key))
						raise NameError("Updating %s FAILED!" %(key))
				
				self.read_rc()
				obj_tmp = {}
				obj_tmp["request"] = uri[0]
				obj_tmp["moisture"] = self.moisture_th
				obj_tmp["watertemp"] = self.watertemp_th
				obj_tmp["precipint"] = self.intprec_th
				obj_tmp["precipprob"] = self.probprec_th
				return json.dumps(obj_tmp)

			else:
				raise NameError("No parameter was correct!")
		else:
			raise NameError("Not a valid URI command!")


	def DELETE(self,*uri,**params):

		#DELETE localhost:8080/res_cat/del_dev?rn=...
		if uri[0]=="del_dev":

			if params.has_key("rn"):
				return self.delete_dev(params["rn"])
			else:
				raise NameError("Input parameter has not correct format!")

		else:
			raise NameError("Not a valid URI command!")
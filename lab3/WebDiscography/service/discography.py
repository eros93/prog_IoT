#!/usr/bin/python

import json
import datetime
import cherrypy
import os,os.path

class WebDiscography(object):
	"""Class Discography
		name: filename
		txt_disc: string containing all the discography
		owner: owner of discography
		update: date of last update
		albums: "dictionary" of class album object
		n: number of album contained into discography
	"""
	exposed=True


	def __init__(self,filename="discography.json"):
		self.name = filename
		self.txt_disc = open(filename, 'r+')
		obj=json.loads(self.txt_disc.read())
		self.txt_disc.close()
		self.owner=obj["discography_owner"]
		self.update=obj["last_update"]
		self.albums={}
		self.n=len(obj["album_list"])
		for x in range(self.n):
			tmp_album=Album(x)
			tmp_album.artist = obj["album_list"][x]["artist"]
			tmp_album.title = obj["album_list"][x]["title"]
			tmp_album.pub_year = obj["album_list"][x]["publication_year"]
			tmp_album.tot_tracks = obj["album_list"][x]["total_tracks"]
			self.albums[str(x)] = tmp_album


	def print_all(self):
		self.txt_disc = open(self.name, 'r')
		all_disc = self.txt_disc.read()
		self.txt_disc.close()
		return all_disc


	def search_by_artist(self,artist):
		result = {}
		result["found_list"]=[]
		tmp_result={}
		flag=0
		for x in range(self.n):
			if self.albums[str(x)].artist.lower() == artist.lower():
				tmp_result["title"] = self.albums[str(x)].title
				tmp_result["pubblication_year"] = self.albums[str(x)].pub_year
				tmp_result["total_tracks"] = self.albums[str(x)].tot_tracks
				result["found_list"].append(tmp_result)
				flag=1

		if flag != 0 :
			return json.dumps(result)
		else :
			return "Artist not found"


	def search_by_title(self,title):
		result = {}
		result["found_list"]=[]
		tmp_result={}
		flag=0
		for x in range(self.n):
			if self.albums[str(x)].title.lower() == title.lower():
				tmp_result["artist"] = self.albums[str(x)].artist
				tmp_result["pubblication_year"] = self.albums[str(x)].pub_year
				tmp_result["total_tracks"] = self.albums[str(x)].tot_tracks
				result["found_list"].append(tmp_result)
				flag=1

		if flag != 0 :
			return json.dumps(result)
		else :
			return result["found_list"].append("Artist not found")


	def search_by_pubblication_year(self,year):
		result = {}
		result["found_list"]=[]
		tmp_result={}
		flag=0
		for x in range(self.n):
			if str(self.albums[str(x)].pub_year) == str(year):
				tmp_result["artist"] = self.albums[str(x)].artist
				tmp_result["title"] = self.albums[str(x)].title
				tmp_result["total_tracks"] = self.albums[str(x)].tot_tracks
				result["found_list"].append(tmp_result)
				flag=1

		if flag != 0 :
			return json.dumps(result)
		else :
			return "Pubblication year not found"


	def search_by_total_tracks(self,tracks):
		result = {}
		result["found_list"]=[]
		tmp_result={}
		flag=0
		for x in range(self.n):
			if str(self.albums[str(x)].tot_tracks) == str(tracks):
				tmp_result["artist"] = self.albums[str(x)].artist
				tmp_result["title"] = self.albums[str(x)].title
				tmp_result["pubblication_year"] = self.albums[str(x)].pub_year
				result["found_list"].append(tmp_result)
				flag=1

		if flag != 0 :
			return json.dumps(result)
		else :
			return "Total tracks not found"


	def insert_new_album(self,new_album):

		self.txt_disc = open(self.name, 'r')
		obj=json.loads(self.txt_disc.read())
		self.txt_disc.close()

		flag = 0
		for x in range(self.n):
			if obj["album_list"][x]["artist"].lower() == new_album["artist"].lower():	#PROBLEMA QUI NON VEDE X COME UN INTERO?
				if obj["album_list"][x]["title"].lower() == new_album["title"].lower():
					flag = 1

		if flag == 1 :
			return "Already inserted"

		else :
			self.n=self.n+1
			time = datetime.datetime.now()
			obj["last_update"] = str(time.replace(second=0,microsecond=0))
			
			obj["album_list"].insert(0,new_album)
			
			self.txt_disc = open(self.name, 'w')
			self.txt_disc.truncate()
			self.txt_disc.write(json.dumps(obj))
			self.txt_disc.close()
			
			return 0

	
	def delete_album(self,album_info):

		self.txt_disc = open(self.name, 'r')
		obj=json.loads(self.txt_disc.read())
		self.txt_disc.close()

		flag = 0
		for x in range(self.n):
			if obj["album_list"][x]["artist"].lower() == album_info["artist"].lower():	#PROBLEMA QUI NON VEDE X COME UN INTERO?
				if obj["album_list"][x]["title"].lower() == album_info["title"].lower():
					hit = x
					flag = 1

		if flag == 0 :
			return "Not found"

		else :
			self.n=self.n-1
			time = datetime.datetime.now()
			obj["last_update"] = str(time.replace(second=0,microsecond=0))
			
			obj["album_list"].pop(hit)
			
			self.txt_disc = open(self.name, 'w')
			self.txt_disc.truncate()
			self.txt_disc.write(json.dumps(obj))
			self.txt_disc.close()
			
			return 0


	def GET(self,*uri,**params):
		if params["idcommand"] == "6":
			all_disc = self.print_all()
			return all_disc


	def POST(self,*uri,**params):
		json_input = cherrypy.request.body.read()
		input_list = json.loads(json_input)
		idcommand = input_list["idcommand"]
		if idcommand == "1" :
			result = self.search_by_artist(input_list["key_word"])
			return result
		elif idcommand == "2" :
			result = self.search_by_title(input_list["key_word"])
			return result
		elif idcommand == "3" :
			result = self.search_by_pubblication_year(input_list["key_word"])
			return result
		elif idcommand == "4" :
			result = self.search_by_total_tracks(input_list["key_word"])
			return result


	def PUT(self,*uri,**params):
		json_input = cherrypy.request.body.read()
		input_list = json.loads(json_input)
		idcommand = input_list["idcommand"]
		
		if idcommand == "5" :
			result = self.insert_new_album(input_list["new_album"])	#vedere esempio json per struttura del json della richiesta PUT_DELETE
			if result == 0:
				input_list["response"] = result		#If Insert is OK --> inputlist["response"] = 0
			else: input_list["response"] = result   #If Insert not done --> inputlist["response"] = "already inserted"
			return json.dumps(input_list)


	def DELETE(self,*uri,**params):
		if params["idcommand"] == "7" :
			input_list={}
			input_list["artist"] =  params["artist"]
			input_list["title"] =  params["title"]
			result = self.delete_album(input_list)	#vedere esempio json per struttura del json della richiesta PUT_DELETE
			if result == 0:
				input_list["response"] = result		#If Insert is OK --> inputlist["response"] = 0
			else: input_list["response"] = result   #If Insert not done --> inputlist["response"] = "not found"
			return json.dumps(input_list)


class Album():
	"""Album class"""
	def __init__(self,id):
		self.id = id
		self.artist = "void"
		self.title = "void"
		self.pub_year = 0
		self.tot_tracks = 0	
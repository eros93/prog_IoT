#!/usr/bin/python

import json

class Discography():

	def __init__(self,filename="discography.json"):
		self.name = filename
		print "\n\tOpening file %r...\n" %filename
		self.txt_disc = open(filename, 'r+')
		obj=json.loads(self.txt_disc.read())		
		self.owner=obj["discography_owner"]
		self.update=obj["last_update"]
		self.albums={}
	#	print obj.items()
		#print obj["album_list"][0]["artist"]
		self.n=len(obj["album_list"])
		for x in range(self.n):
			tmp_album=Album(x)
			tmp_album.artist = obj["album_list"][x]["artist"]
			tmp_album.title = obj["album_list"][x]["title"]
			tmp_album.pub_year = obj["album_list"][x]["publication_year"]
			tmp_album.tot_tracks = obj["album_list"][x]["total_tracks"]
			self.albums[str(x)] = tmp_album

#		print self.albums["1"].pub_year

	def print_all(self):
		print self.txt_disc.read()
		return

	def search_by_artist(self,artist):
		print ("\n\tAlbums found for Artist: "+artist)
		for x in range(self.n):
			if self.albums[str(x)].artist.lower() == artist.lower():
				print ("\n\t\tTitle: "+self.albums[str(x)].title)
				print ("\n\t\tPublication year: %d" %self.albums[str(x)].pub_year)
				print ("\n\t\tTotal_tracks : %d" %self.albums[str(x)].tot_tracks)
				print "\n"				

	def search_by_title(self,title):
		print "\n\tSearching for %r in title...\n" %title

	def search_by_pubblication_year(self,year):
		print "\n\tSearching for %r in pubblication year...\n" %year

	def search_by_total_tracks(self,tracks):
		print "\n\tSearching for %r in total tracks...\n" %tracks



class Album():
	"""docstring for album"""
	def __init__(self,id):
		self.id = id
		self.artist = "void"
		self.title = "void"
		self.pub_year = 0
		self.tot_tracks = 0

		
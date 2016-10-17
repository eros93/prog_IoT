#!/usr/bin/python

import json
import datetime

class Discography():
	"""Class Discography
		name: filename
		txt_disc: string containing all the discography
		owner: owner of discography
		update: date of last update
		albums: "dictionary" of class album object
		n: number of album contained into discography
	"""
	def __init__(self,filename="discography.json"):
		self.name = filename
		print "\n\tOpening file %r...\n" %filename
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
		print self.txt_disc.read()
		self.txt_disc.close()
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
		print ("\n\tAlbums found for Title: "+title)
		for x in range(self.n):
			if self.albums[str(x)].title.lower() == title.lower():
				print ("\n\t\tArtist: "+self.albums[str(x)].artist)
				print ("\n\t\tPublication year: %d" %self.albums[str(x)].pub_year)
				print ("\n\t\tTotal_tracks : %d" %self.albums[str(x)].tot_tracks)
				print "\n"

	def search_by_pubblication_year(self,year):
		print ("\n\tAlbums found for Year: "+str(year))
		for x in range(self.n):
			if str(self.albums[str(x)].pub_year) == str(year):
				print ("\n\t\tArtist: "+self.albums[str(x)].artist)
				print ("\n\t\tTitle: "+self.albums[str(x)].title)
				print ("\n\t\tTotal_tracks : %d" %self.albums[str(x)].tot_tracks)
				print "\n"

	def search_by_total_tracks(self,tracks):
		print ("\n\tAlbums found for Total tracks: "+str(tracks))
		for x in range(self.n):
			if str(self.albums[str(x)].tot_tracks) == str(tracks):
				print ("\n\t\tArtist: "+self.albums[str(x)].artist)
				print ("\n\t\tTitle: "+self.albums[str(x)].title)
				print ("\n\t\tPublication year: %d" %self.albums[str(x)].pub_year)
				print "\n"

	def insert_new_album(self,new_album):
		self.n=self.n+1
		
		self.txt_disc = open(self.name, 'r')
		obj=json.loads(self.txt_disc.read())
		self.txt_disc.close()

		time = datetime.datetime.now()
		obj["last_update"] = str(time.replace(second=0,microsecond=0))
		obj["album_list"].insert(0,new_album)

		self.txt_disc = open(self.name, 'w')
		self.txt_disc.truncate()
		self.txt_disc.write(json.dumps(obj))
		self.txt_disc.close()


class Album():
	"""Album class"""
	def __init__(self,id):
		self.id = id
		self.artist = "void"
		self.title = "void"
		self.pub_year = 0
		self.tot_tracks = 0	
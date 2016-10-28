#!/usr/bin/python
import os,os.path
import cherrypy
import json
from cherrypy.lib.static import serve_file

class FreeboardAgent(object):
	
	exposed=True
	def __init__(self,id):
		self.id = id

	def GET(self,*uri,**params):
		#pathname=(os.path.abspath(os.getcwd())+"/index.html")
		n=len(uri)
		path=(os.path.abspath(os.getcwd()))+"/"
		for x in range(n):
			path=path+str(uri[x])+"/"
#		return path
		return serve_file(path)
#		return os.path.abspath(os.getcwd())

if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True,
			'tools.staticdir.root':os.path.abspath(os.getcwd()) #this function return the path where the main.py is stored
		},
		# '/freeboard':{
		# 	'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
		# 	'tools.staticdir.on':True,
		# 	'tools.staticdir.dir':'./freeboard', #this static assigment is the path of freeboard (it must be in the same folder of main.py)
		# },
		'js/freeboard.thirdparty.min.js':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
			'tools.staticdir.on':True,
			'tools.staticdir.dir':'./js/freeboard.thirdparty.min.js'
		},
		'css/freeboard.min.css':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(), 
			'tools.staticdir.on':True,
			'tools.staticdir.dir':'./css/freeboard.min.css'
		}
	}
	cherrypy.tree.mount(FreeboardAgent(1), '/',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()


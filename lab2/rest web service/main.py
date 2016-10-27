#!/usr/bin/python
import os,os.path
import cherrypy
import json

class FreeboardAgent(object):
	
	exposed=True
	def __init__(self,id):
		self.id = id

	def GET(self,*uri,**params):
		return str(uri[0])

if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True,
			'tools.staticdir.root':os.path.abspath(os.getcwd())
		},
		'/static':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.staticdir.on':True,
			'tools.staticdir.dir':'./freeboard'
		}
	}
	cherrypy.tree.mount(FreeboardAgent(1), '/static',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()


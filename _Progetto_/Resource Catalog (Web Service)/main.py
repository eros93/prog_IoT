import cherrypy
import os, os.path
from res_cat_lib import ResourceCatalog

if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True,
			'tools.staticdir.root':os.path.abspath(os.getcwd()) #this function return the path where the main.py is stored
		},
		'/res_cat':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True
		}
	}
	cherrypy.tree.mount(ResourceCatalog(1), '/res_cat', conf)
	#cherrypy.server.socket_host = '10.42.0.1'
	#cherrypy.server.socket_host = '192.168.1.71'
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.engine.start()
	cherrypy.engine.block()
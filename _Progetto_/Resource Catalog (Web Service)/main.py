import cherrypy
import cherrypy.lib
import os, os.path
from res_cat_lib import ResourceCatalog

if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			#'tools.sessions.on':True,
			'tools.staticdir.root':os.path.abspath(os.getcwd()), #this function return the path where the main.py is stored
			#'tools.sessions.secure':True,
			'tools.response_headers.on': True,
			'tools.response_headers.headers': [('Content-Type', 'application/json')]
		},
		'/res_cat':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			#'tools.sessions.on':True,
			#'tools.sessions.secure':True,
			#'tools.response_headers.on': True,
			#'tools.response_headers.headers': [('Content-Type', 'application/json; charset=utf-8')]
		}
	}
	cherrypy.tree.mount(ResourceCatalog(1), '/res_cat', conf)
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.engine.start()
	cherrypy.engine.block()
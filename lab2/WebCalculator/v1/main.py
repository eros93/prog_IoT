#!/usr/bin/python

from calculator import WebCalculator
import cherrypy


if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True
		}
	}
	cherrypy.tree.mount(WebCalculator(1), '/',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
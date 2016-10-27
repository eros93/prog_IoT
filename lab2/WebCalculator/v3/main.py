#!/usr/bin/python

from calculator import WebCalculatorV2
import cherrypy


if __name__ == "__main__":
	conf = {
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True
		}
	}
	cherrypy.tree.mount(WebCalculatorV2(1), '/',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
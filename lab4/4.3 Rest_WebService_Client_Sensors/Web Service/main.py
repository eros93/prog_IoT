
from websensor import WebSensor
import cherrypy
import os,os.path

if __name__ == "__main__":
    # cherrypy.config.update({'server.socket_host':'192.168.1.254','server.socket_port':8080})
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True,
            'tools.staticdir.root':os.path.abspath(os.getcwd())
        }
    }
    cherrypy.tree.mount(WebSensor(1), '/',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

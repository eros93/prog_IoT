#Web service for elaboration of data from 

from bikewebservice import BikeWebService
import cherrypy

if __name__ == "__main__":
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True
        }
    }
    cherrypy.tree.mount(BikeWebService(1), '/',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

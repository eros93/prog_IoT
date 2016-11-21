#Program to managing a Discography
# -----> python main.py [filename_discography.json]

from discography import WebDiscography
import cherrypy
import os,os.path

if __name__ == "__main__":
    conf = {
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True,
            'tools.staticdir.root':os.path.abspath(os.getcwd())
        }
    }
    cherrypy.tree.mount(WebDiscography(), '/',conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

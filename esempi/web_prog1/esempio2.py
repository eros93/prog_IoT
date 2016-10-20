import cherrypy

class Generator(object):

	def hello(self,* uri,** params):
		return open('./hello/hello_form.html', 'r').read()

	hello.exposed = True

	def replay(self,* uri,** params):
		return open('./hello/page.html', 'r').read()

	replay.exposed = True


if __name__=='__main__':
	cherrypy.tree.mount(Generator(), '/')
	cherrypy.engine.start()
	cherrypy.engine.block()



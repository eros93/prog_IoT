# ciao enrico ... i love you 


import cherrypy

class Generator(object):

	def index(self,* uri,** params):
		return '''<form action="replay" method= "POST">
		Sequence (in FASTA format):<br />
		<textarea name="seq" rows="10" cols="80" /></textarea><br />
		<input type="submit" />
		</form>
		'''

	index.exposed = True

	def replay(self,* uri,** params):
		return open('./hello/page.html', 'r').read()

	replay.exposed = True

if __name__=='__main__':
	cherrypy.tree.mount(Generator(), '/')
	cherrypy.engine.start()
	cherrypy.engine.block()
from http.server import HTTPServer, BaseHTTPRequestHandler
from string import Template


t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')

pages = ['about', 'homepage', 'contacts']

nav = ''
for page in pages:
	a = f'<a href="/{page}">{page}</a>'
	nav += a


class ExtendedHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
#		print('before logging request')
		#print(self.headers)
		print('path:', self.path)
		
		if self.path.endswith('.css'):
			self.send_response(200)
			self.send_header('Content-type', 'text/css')
			self.end_headers()

			with open('style.css', 'r', encoding='utf-8') as styles:
				self.wfile.write(styles.read().encode('utf-8'))
				return

		#if self.path == '/':
		#	content = 'homepage'
		#else:
		#	content = 'elsewhere'
#		print('after logging request')
		self.send_response(200)
		self.send_header('Content-type','text/html')#'text/plain')
		self.end_headers()



		#script = '<script>alert(\'wow\')</script>'
		#template = Template('2$script')
		#a = template.substitute(script=script)

		self.wfile.write('<link rel="stylesheet" href="style.css">'.encode('utf-8'))
		self.wfile.write(nav.encode('utf-8'))
		self.wfile.write('wow'.encode('utf-8'))
		#self.wfile.write(a.encode('utf-8'))
		#self.wfile.write(script.encode('utf-8'))
#		self.wfile.write(f'{f} {message} {content} {script}'.encode('utf-8'))
#		self.wfile.write('Hello, lol1world! from $content'.encode('utf-8'))
		return

def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

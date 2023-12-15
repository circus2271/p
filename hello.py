from http.server import HTTPServer, BaseHTTPRequestHandler
from string import Template


t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')


class ExtendedHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
#		print('before logging request')
		#print(self.headers)
		print('path:', self.path)

		if self.path == '/':
			content = 'homepage'
		else:
			content = 'elsewhere'
#		print('after logging request')
		self.send_response(200)
		self.send_header('Content-type','text/plain')
		self.end_headers()

		self.wfile.write(f'{f} {message} {content}'.encode('utf-8'))
#		self.wfile.write('Hello, lol1world! from $content'.encode('utf-8'))
		return

def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from string import Template


t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')

pages = ['', 'about', 'homepage', 'contacts']


def nav(current_url):
	parts = ['<nav><ul>']
	for page in pages:
		is_active = 'active' if page == current_url else ''
		li = f'<li><a href="/{page}" class="{is_active}">{page}</a></li>'
		parts.append(li)
	parts.append('</ul></nav>')
	html = ''.join(parts)
	return html

cache = {}

with open(f'./particles/footer.html') as f:
	cache['footer'] = f.read()

class ExtendedHTTPRequestHandler(SimpleHTTPRequestHandler):

	def do_GET(self):
		print('path:', self.path)
		current_url = self.path[1:]
		# if True:
		
		if current_url not in pages:

		#if self.path.endswith('.css'):
			super().do_GET()
			return

		if current_url == '':
			page = 'homepage'
		else:
			page = current_url

		self.send_response(200)
		self.send_header('Content-type','text/html')#'text/plain')
		self.end_headers()

		self.wfile.write('<link rel="stylesheet" href="style.css">'.encode('utf-8'))
		self.wfile.write(nav(current_url).encode('utf-8'))

		if page in cache:
			particle = cache[page]
		else:
			with open(f'./particles/{page}.html') as p:
				particle = p.read()
				cache[page] = particle
		self.wfile.write(particle.encode('utf-8'))

		footer = cache['footer']
		self.wfile.write(footer.encode('utf-8'))


		self.wfile.write('wow'.encode('utf-8'))
		return

def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

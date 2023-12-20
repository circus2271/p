from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from string import Template

from jinja2 import Environment, PackageLoader, select_autoescape, TemplateNotFound

env = Environment(
    loader=PackageLoader('hello'),
    autoescape=select_autoescape()
)


navlinks = (
    {
        'name': 'homepage',
        'url': '/'
    },
    {
        'name': 'about',
        'url': '/about'
    },
    {
        'name': 'contacts',
        'url': '/contacts'
    },
    {
        'name': 'no_template',
        'url': '/no_template'
    }
)

#print(template.render(navlinks=navlinks, current_page='contacts'))

t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')


# pages = ['homepage', 'about', 'contacts', 'no_template']

class ExtendedHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print('path:', self.path)
        current_url = self.path
        # if True:

        # if current_url not in pages:
        #if current_url.startswith('/assets'):
        if self.path.startswith('/assets'):
            super().do_GET()
            return

        #if current_url == '':
        #    curent_page = 'homepage'
        #else:
        #    curent_page = current_url

        if current_url == '/':
            template_name = 'index'
        else:
            template_name = current_url[1:] # remove slash from url start

        try:
            template = env.get_template(f'{template_name}.html')
        except TemplateNotFound:
            self.send_error(404, message="Template not found")
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        self.wfile.write(template.render(navlinks=navlinks, current_url=current_url).encode('utf-8'))

        self.wfile.write('wow'.encode('utf-8'))
        return


def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

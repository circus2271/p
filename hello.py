from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from string import Template
from datetime import date

from jinja2 import Environment, PackageLoader, select_autoescape, TemplateNotFound

env = Environment(
    loader=PackageLoader('hello'),
    autoescape=select_autoescape()
)


navlinks = [
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
]

predefined_links = [link['url'] for link in navlinks]

t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')


events = [
    {
        'title': 'wow new event',
        'description': 'wow description',
        'date': 'today',
        'id': 1
    },
    {
        'title': 'wow second new event',
        'description': 'wow new second event description',
        'date': 'friday 2024',
        'id': 2
    },
]

class ExtendedHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print('path:', self.path)
        current_url = self.path

        if current_url.startswith('/assets'):
            super().do_GET()
            return

        if current_url in predefined_links:
            if current_url == '/':
                template_name = 'index.html'
            else:
                template_name = f'{current_url[1:]}.html'

            try:
                template = env.get_template(template_name)
            except TemplateNotFound:
                self.send_header('Content-type', 'text/html')
                self.send_error(404, message="Template not found")
                return

            context = {
                'navlinks': navlinks,
                'current_url': current_url,
                'current_year': date.today().strftime('%Y')
            }

            if current_url == '/':
                context['events'] = events

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            self.wfile.write(template.render(context=context).encode('utf-8'))
            return

        if current_url not in predefined_links:
            # maybe it's an event detail page
            # find event by its id
            # if matches, show its detail page
            current_event = None
            for event in events:
                print('event id', str(event['id']))
                if current_url[1:] == str(event['id']):
                    current_event = event
                    break

            if current_event:
                print('curenene', current_event)
                # print(template_name == str(event['id']))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template = env.get_template('event.html')
                context = {
                    'navlinks': navlinks,
                    'current_url': current_url,
                    'event': events[current_event['id'] - 1],
                    'current_year': date.today().strftime('%Y')
                }
                self.wfile.write(template.render(context=context).encode('utf-8'))

                return

            # unknown page, show error
            self.send_error(404)
            return


def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from string import Template

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

available_pages = [link['url'] for link in navlinks]
#print(template.render(navlinks=navlinks, current_page='contacts'))

t = Template('Hello, $name')
message = t.substitute(name='Ivan')

name = 'format'
f = f'hello {name}'

print('hello from python script')


# pages = ['homepage', 'about', 'contacts', 'no_template']

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


        if current_url not in available_pages:
            cur_enent = None
            for event in events:
                print('templaten', template_name)
                print('event id', str(event['id']))
                # print(template_name == str(event['id']))
                # if template_name == str(event['id']):
                #     break
                if current_url[1:] == str(event['id']):
                    # template = env.get_template('event.html')
                    cur_enent = event
                    break

            if cur_enent:
                print('curenene', cur_enent)
                # print(template_name == str(event['id']))
                self.send_header('Content-type', 'text/html')
                self.send_response(200)
                self.end_headers()

                template = env.get_template('event.html')
                print(template.render(event=cur_enent))
                self.wfile.write(template.render(navlinks=navlinks, current_url=current_url, event=events[0]).encode('utf-8'))

             #   self.wfile.write(template.render(event=cur_enent, navlinks=navlinks, current_url=current_url,).encode('utf-8'))
                return

            self.send_error(404, message="..Template not found")
            return

        try:
            template = env.get_template(f'{template_name}.html')
        except TemplateNotFound:
            self.send_header('Content-type', 'text/html')

            self.send_error(404, message="Template not found")
            return


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # if template_name == 'index':
        #     events = [
        #
        #     ]

        self.wfile.write(template.render(navlinks=navlinks, current_url=current_url, events=events).encode('utf-8'))

        self.wfile.write('wow'.encode('utf-8'))
        return


def run(server_class=HTTPServer, handler_class=ExtendedHTTPRequestHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

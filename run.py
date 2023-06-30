from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load
from gevent import pywsgi
import socket

if __name__ == '__main__':

    # Load configuration from config.json
    config = load(open('config.json', 'r'))
    site_config = config['site_config']

    # Set up the website routes
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Run the Flask server by WSGI
    print(f"Running on http://127.0.0.1:{site_config['port']}")
    print(f"Running on http://{ip_address}:{site_config['port']}")
    
    server = pywsgi.WSGIServer(('0.0.0.0', site_config['port']), app)
    server.serve_forever()
    
    print(f"Closing {ip_address}:{site_config['port']}")
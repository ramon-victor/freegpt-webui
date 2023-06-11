import subprocess
import os
from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load


def start_gpt4api():
    # Get the GPT-4 API directory path
    api_directory = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "apiGPT4")

    # Install the GPT-4 dependencies using yarn
    install_dependencies = subprocess.Popen(
        ["yarn"], cwd=api_directory, shell=True)
    install_dependencies.wait()

    # Start the GPT-4 process using yarn start
    api_process = subprocess.Popen(
        ["yarn", "start"], cwd=api_directory, shell=True)

    return api_process


if __name__ == '__main__':
    # Run GPT-4 API
    gpt4api_process = start_gpt4api()

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

    # Run the Flask server
    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")

    # Terminate the GPT-4 API process when the Flask server is closed
    gpt4api_process.terminate()

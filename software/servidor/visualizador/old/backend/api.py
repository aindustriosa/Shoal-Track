"""
This script runs the API_REST application using a development server.
"""

from os import environ
from API_REST import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        #PORT = int(environ.get('SERVER_PORT', '5555'))
        PORT = 4999
    except ValueError:
        PORT = 5555
    app.run("0.0.0.0", PORT,use_reloader=False)

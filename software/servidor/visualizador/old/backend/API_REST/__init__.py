"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

import API_REST.views

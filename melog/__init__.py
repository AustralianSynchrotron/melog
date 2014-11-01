from flask import Flask
from flask.ext.plugins import PluginManager
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_FOLDER = os.path.join(BASE_DIR,"plugins/")

app = Flask(__name__)

#initialise the plugin manager
#plugin_manager = PluginManager(app,plugin_folder=PLUGIN_FOLDER)
plugin_manager = PluginManager(app)

import melog.config
import melog.views

#http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database


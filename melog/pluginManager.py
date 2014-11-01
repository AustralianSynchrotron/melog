#http://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
import imp
import os
from flask import current_app
from flask.ext.plugins import Plugin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_FOLDER = os.path.join(BASE_DIR,"plugins/")
MAIN_MODULE = "__init__"

def getPlugins():
    plugins = []
    possiblePlugs = os.listdir(PLUGIN_FOLDER)
    for i in possiblePlugs:
        plugPath = os.path.join(PLUGIN_FOLDER,i)

        #check if the plugPath is a folder and contain __init__.py...
        if not os.path.isdir(plugPath) or not MAIN_MODULE + ".py" in os.listdir(plugPath):
            continue

        info = imp.find_module(MAIN_MODULE,[plugPath])
        plugins.append({"name": i, "info": info})

    return plugins

def loadPlugin(plugin):
    return imp.load_module(MAIN_MODULE, *plugin["info"])


class AppPlugin(Plugin):
    def register_blueprint(self, blueprint, **kwargs):
        """Registers a blueprint."""
        current_app.register_blueprint(blueprint, **kwargs)
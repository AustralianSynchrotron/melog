from flask import Blueprint, render_template
from melog.pluginManager import AppPlugin

__plugin__ = "handover"
__version__ = "0.1"

handover = Blueprint("handover",__name__,template_folder="templates")
#handover = Blueprint("handover",__name__)

@handover.route("/")
def index():
    return "handover Plugin Active..."
    #return render_template()

class Handover(AppPlugin):
    def setup(self):
        self.register_blueprint(handover, url_prefix="/handover")

    def install(self):
        pass

    def uninstall(self):
        pass
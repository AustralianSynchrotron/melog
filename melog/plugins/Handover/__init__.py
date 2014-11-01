from flask import Blueprint, render_template
from melog.pluginManager import AppPlugin

__plugin__ = "Handover"
__version__ = "0.1"

handover = Blueprint("Handover",__name__,template_folder="templates")

@handover.route("/")
def index():
    return "Handover Plugin Active..."
    #return render_template()

class Handover(AppPlugin):
    def setup(self):
        self.register_blueprint(Handover, url_prefix="/handover")
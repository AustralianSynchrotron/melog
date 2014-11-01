from flask import Blueprint, render_template
from melog.pluginManager import AppPlugin

__plugin__ = "Handover"
__version__ = "0.1"

Handover = Blueprint("Handover",__name__,template_folder="templates")

@Handover.route("/")
def index():
    return "Handover Plugin Active..."

class Handover(AppPlugin):
    def setup(self):
        self.register_blueprint(Handover, url_prefix="/handover")
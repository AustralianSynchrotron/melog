from flask import Flask,render_template

app = Flask(__name__)

import melog.config
import melog.views

#http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database


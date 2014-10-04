from flask import render_template
from melog import app
from melog.models import ElogGroupData,ElogData

@app.route('/')
def meLog():
    groups = ElogGroupData.query.all()
    return render_template("index.html", groups=groups)
    #return render_template("index.html")
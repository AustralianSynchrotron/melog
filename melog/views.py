from flask import render_template
from melog import app
from melog.models import ElogGroupData,ElogData
from datetime import datetime

@app.route('/')
def meLog():
    groups = ElogGroupData.query.filter(ElogGroupData.private == 0)
    time = datetime.now().time().strftime("%H:%M:%S")
    date = datetime.now().date()
    return render_template("index.html", timestamp=time, datestamp=date, groups=groups)
    #return render_template("index.html")

@app.route('/test/')
def Test():
    return render_template("test_edit.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
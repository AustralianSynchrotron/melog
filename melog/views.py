from flask import render_template
from melog import app
from melog.models import ElogGroupData,ElogData
from datetime import datetime

@app.route('/<group>/<int:year>/<int:month>/<int:day>/')
@app.route('/<group>/',defaults={'year':None,'month':None,'day':None})
@app.route('/',defaults={'group':None,'year':None,'month':None,'day':None})
def meLog(group,year,month,day):
    groups = ElogGroupData.query.filter(ElogGroupData.private == 0).order_by(ElogGroupData.sort)
    eLog = ElogData.query.limit(5).all()
    time = datetime.now().time().strftime("%H:%M:%S")
    date = datetime.now().date()
    return render_template("index.html", timestamp=time, datestamp=date, groups=groups, elogEntry=eLog)
    #return render_template("index.html")

@app.route('/test/')
def Test():
    return render_template("test_edit.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
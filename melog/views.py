from flask import render_template,session,redirect,url_for,request
from melog import app
from config import data
from melog.models import ElogGroupData,ElogData,SolUsers
from datetime import datetime
import ldap

#Useful links
#http://flask.pocoo.org/docs/0.10/quickstart/
#https://pythonhosted.org/Flask-SQLAlchemy/index.html
#http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/

@app.route('/<urlGroup>/<int:year>/<int:month>/<int:day>/')
@app.route('/<urlGroup>/',defaults={'year':None,'month':None,'day':None})
@app.route('/',defaults={'group':None,'year':None,'month':None,'day':None})
def meLog(urlGroup,year,month,day):
    if 'username' not in session:
        return redirect(url_for('Login'))

    #required for backwards compatibility
    if request.args.get('y'):
        year = request.args.get('y')

    if request.args.get('m'):
        month = request.args.get('m')

    if request.args.get('d'):
        day = request.args.get('d')

    if urlGroup != None:
        tmpGroup = ElogGroupData.query.filter(ElogGroupData.urlName == urlGroup).first_or_404()
        group = tmpGroup.group_title
        #app.logger.debug(urlGroup.group_title)
    # else load the default
    else:
        group = session['group']
        urlGroup = ElogGroupData.query.filter(ElogGroupData.group_title == group).first_or_404()

    time = datetime.now().time().strftime("%H:%M:%S")
    date = datetime.now().date()

    groups = ElogGroupData.query.filter(ElogGroupData.private == 0).order_by(ElogGroupData.sort)
    eLog = ElogData.query.filter(ElogData.created > date).from_self().order_by(ElogData.created)

    return render_template("index.html", timestamp=time, datestamp=date, groups=groups, default_group=group, elogEntry=eLog)
    #return render_template("index.html")

@app.route('/test/')
def Test():
    return render_template("test_edit.html")

@app.route('/login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        username = request.form['text-name']
        password = request.form['text-pass']

        if ((username == "") or (password == "")):
            return redirect(url_for('Login'))

        ldap_server = "ldap://"+data['ldap_server']
        ldap_dn = data['ldap_dn']
        ldap_sx = data['ldap_sx']
        connect = ldap.initialize(ldap_server)

        #attempt bind to ldap, if it fails, then try again
        try:
            connect.simple_bind_s(username+ldap_sx,password)

        except ldap.LDAPError,e:
            #Failed login unbind and return to login screen
            connect.unbind_s()
            return render_template("login.html", error=e)

        #if success
        tmp_group = SolUsers.query.filter(SolUsers.username == username).first_or_404()
        default_group = ElogGroupData.query.filter(ElogGroupData.group_id == tmp_group.gid).first_or_404()
        #app.logger.debug(default_group.urlName)

        #assign session variables
        session['username'] = username
        session['group'] = default_group.group_title

        return redirect("/%s" % default_group.urlName)
            #return render_template("index.html")

    else:
        #if GET request just display the login page
        return render_template("login.html")

@app.route('/logout')
def Logout():
    session.pop('username',None)
    return redirect(url_for('Login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
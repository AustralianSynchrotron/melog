from flask import render_template,session,redirect,url_for,request
from melog import app
from config import data
from melog.models import ElogGroupData,ElogData
from datetime import datetime
import ldap

#Useful links
#http://flask.pocoo.org/docs/0.10/quickstart/
#https://pythonhosted.org/Flask-SQLAlchemy/index.html
#http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/

@app.route('/<group>/<int:year>/<int:month>/<int:day>/')
@app.route('/<group>/',defaults={'year':None,'month':None,'day':None})
@app.route('/',defaults={'group':None,'year':None,'month':None,'day':None})
def meLog(group,year,month,day):
    if 'username' not in session:
        return redirect(url_for('Login'))

    if group != None:
        urlGroup = ElogGroupData.query.filter(ElogGroupData.urlName == group).first_or_404()
        app.logger.debug(urlGroup.group_title)
    # else load the default
    time = datetime.now().time().strftime("%H:%M:%S")
    date = datetime.now().date()

    groups = ElogGroupData.query.filter(ElogGroupData.private == 0).order_by(ElogGroupData.sort)
    eLog = ElogData.query.filter(ElogData.created > date).from_self().order_by(ElogData.created)

    return render_template("index.html", timestamp=time, datestamp=date, groups=groups, elogEntry=eLog)
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
        try:
            connect.simple_bind_s(username+ldap_sx,password)
            connect.search_s(ldap_dn,ldap.SCOPE_SUBTREE,
                                  '(&(objectclass=User) (sAMAccountName='+username+'))',
                                  ['title','displayName','givenName'])

            session['username'] = username
            return redirect(url_for('meLog'))

        except ldap.LDAPError,e:
            #Failed login unbind and return to login screen
            connect.unbind_s()
            return render_template("login.html", error=e)

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
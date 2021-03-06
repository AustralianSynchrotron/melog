from flask import render_template,session,redirect,url_for,request,current_app
from melog import app
from config import data
from melog.models import ElogGroupData,ElogGroups,ElogData,SolUsers
from melog.database import db
from sqlalchemy.sql import extract,and_,or_
from datetime import datetime
import ldap
from flask.ext.plugins import get_plugins_list

available_plugins = get_plugins_list()
app.logger.debug(available_plugins)
#Useful links
#http://flask.pocoo.org/docs/0.10/quickstart/
#https://pythonhosted.org/Flask-SQLAlchemy/index.html
#http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
#http://www.lfd.uci.edu/~gohlke/pythonlibs/

@app.route('/<urlGroup>/<int:year>/<int:month>/<int:day>/', methods=['GET','POST'])
@app.route('/<urlGroup>/<int:year>/<int:month>/',defaults={'day':None})
@app.route('/<urlGroup>/<int:year>/',defaults={'month':None,'day':None})
@app.route('/<urlGroup>/',defaults={'year':None,'month':None,'day':None})
@app.route('/',defaults={'urlGroup':None,'year':None,'month':None,'day':None})
def meLog(urlGroup,year,month,day):
    if 'username' not in session:
        return redirect(url_for('Login'))
        #might need to change this to allow headless data posting from external apps (Matlab, ALH etc)

    if request.method == 'POST':
        #TODO: need some error checking on these inputs
        author = request.form['text-author']
        title = request.form['text-title']
        date = request.form['text-date']
        time = request.form['text-time']
        text = request.form['text-edit']

        #Convert the date and time strings into a datetime object
        strDateTime = "%s %s" % (date,time)
        dtDateTime = datetime.strptime(strDateTime,"%Y-%m-%d %H:%M:%S") #2014-10-20 21:52:07

        #Need the group_id to update the elog groups table
        tmpGroup = ElogGroupData.query.filter(ElogGroupData.urlName == urlGroup).first_or_404()
        groupNum = tmpGroup.group_id

        #create the db object to write to db
        entry = ElogData(title=title,author=author,created=dtDateTime,text=text,read_only=0)
        db.session.add(entry)
        db.session.flush() #flush the session to get the primary key of the yet to be inserted ElogData
        groups = ElogGroups(entry_id=entry.entry_id,group_id=groupNum)
        db.session.add(groups)
        db.session.commit() #now write the changes to the db

        return redirect("/%s/%s/%s/%s/" % (urlGroup,year,month,day))

    else:
        #required for backwards compatibility with sol2 - Is this needed?
        if request.args.get('y'):
            year = request.args.get('y')

        if request.args.get('m'):
            month = request.args.get('m')

        if request.args.get('d'):
            day = request.args.get('d')

        # get the current date and time
        time = datetime.now().time().strftime("%H:%M:%S")
        date = datetime.now().date()
        defaultDate = False
        defaultYear = False
        defaultMonth = False
        defaultDay = False

        # If year not specified use current
        if not year:
            year = date.year
            defaultDate = True
            defaultYear = True

        # If month not specified use current
        if not month:
            month = date.month
            defaultDate = True
            defaultMonth = True

        # If day not specified use current
        if not day:
            day = date.day
            defaultDate = True
            defaultDay = True

        #use the urlGroup var if specified
        if urlGroup != None:
            tmpGroup = ElogGroupData.query.filter(ElogGroupData.urlName == urlGroup).first_or_404()
            group = tmpGroup.group_title
            groupNum = tmpGroup.group_id
        # else load the default
        else:
            group = session['group']
            tmpGroup = ElogGroupData.query.filter(ElogGroupData.group_title == group).first_or_404()
            urlGroup = tmpGroup.urlName
            groupNum = tmpGroup.group_id

        #Get a list of available groups for select menu display
        groups = ElogGroupData.query.filter(ElogGroupData.private == 0).order_by(ElogGroupData.sort)

        if defaultDate:
            if defaultYear:
                #Get the relevent log entries for group(if no date specified - then todays date as default)
                eLogJoin = ElogData.query.join(ElogGroups,(ElogGroups.entry_id == ElogData.entry_id)) \
                                        .filter(ElogData.created > date,ElogGroups.group_id == groupNum) \
                                        .from_self() \
                                        .order_by(ElogData.created.desc())
            elif defaultMonth:
                #use supplied year var and defaults for the rest
                eLogJoin = ElogData.query.join(ElogGroups,(ElogGroups.entry_id == ElogData.entry_id)) \
                                        .filter(ElogGroups.group_id == groupNum) \
                                        .filter(extract('year',ElogData.created) == year) \
                                        .from_self() \
                                        .order_by(ElogData.created.desc())
            elif defaultDay:
                #use supplied year and month vars and defaults for the rest
                eLogJoin = ElogData.query.join(ElogGroups,(ElogGroups.entry_id == ElogData.entry_id)) \
                                        .filter(ElogGroups.group_id == groupNum) \
                                        .filter(extract('year',ElogData.created) == year) \
                                        .filter(extract('month',ElogData.created) == month) \
                                        .from_self() \
                                        .order_by(ElogData.created.desc())
        else:
            #get the entries based on the supplied date information
            eLogJoin = ElogData.query.join(ElogGroups,(ElogGroups.entry_id == ElogData.entry_id)) \
                                    .filter(ElogGroups.group_id == groupNum) \
                                    .filter(extract('year',ElogData.created) == year) \
                                    .filter(extract('month',ElogData.created) == month) \
                                    .filter(extract('day',ElogData.created) == day) \
                                    .from_self() \
                                    .order_by(ElogData.created.desc())

        #Reformat the provided date for navigation display
        tmpDate = "%s %s %s" % (year,month,day)
        strDate = datetime.strptime(tmpDate,"%Y %m %d").strftime("%a %d %b %Y")

        return render_template("index.html", year=year, month=month, day=day, timestamp=time, datestamp=date, formatDate=strDate,
                               groups=groups, default_group=group, url_group=urlGroup, elogEntry=eLogJoin)
        #return render_template("index.html")

@app.route('/search/', methods=['POST'])
def Search():
    if request.method == 'POST':
        searchGroup = request.form['search-group']
        searchText = request.form['search-text']
        searchTextList = searchText.split(" ")
        searchTextList = [str(x) for x in searchTextList]
        # http://stackoverflow.com/questions/2640628/sqlalchemy-an-efficient-better-select-by-primary-keys
        # http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.ColumnProperty.Comparator
        searchFilter = and_( * [ElogData.text.contains(x) for x in searchTextList])

        eLogSearch = ElogData.query.join(ElogGroups,(ElogGroups.entry_id == ElogData.entry_id)) \
                                    .filter(ElogGroups.group_id == searchGroup) \
                                    .filter(searchFilter) \
                                    .from_self() \
                                    .order_by(ElogData.created.desc())

        groups = ElogGroupData.query.filter(ElogGroupData.private == 0).order_by(ElogGroupData.sort)

        #return "Search for %s: list %s: filters %s: query %s" % (searchText, searchTextList, searchFilter, eLogSearch)
        return render_template("search.html",elogEntry=eLogSearch, groups=groups, searchText=searchTextList)

@app.route('/test/')
def Test():
    #A page holder for testing things
    return render_template("test_edit.html")

@app.route('/login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        username = request.form['text-name']
        password = request.form['text-pass']

        #Make sure there are no blank values - simple test, maybe need more?
        if ((username == "") or (password == "")):
            return redirect(url_for('Login'))

        #load the ldap setting from the config.json
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
            return render_template("login.html", error=e) #maybe provide more user friendly error message

        #if success
        tmp_group = SolUsers.query.filter(SolUsers.username == username).first_or_404()
        default_group = ElogGroupData.query.filter(ElogGroupData.group_id == tmp_group.gid).first_or_404()
        #app.logger.debug(default_group.urlName)

        #assign session variables for convenient later reference
        session['username'] = username
        session['group'] = default_group.group_title

        return redirect("/%s" % default_group.urlName)
            #return render_template("index.html")

    else:
        #if GET request just display the login page
        return render_template("login.html")

@app.route('/logout')
def Logout():
    #remove session vars will logout
    session.pop('username',None)
    session.pop('group',None)
    return redirect(url_for('Login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
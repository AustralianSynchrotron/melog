from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy
import json

json_data=open('config.json')
data = json.load(json_data)
json_data.close()

username = data['dbuser']
password = data['password']
host = data['host']
db_name = data['database']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (username,password,host,db_name)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host:port/db_name'
db = SQLAlchemy(app)
db.Model.metadata.reflect[db.engine]

class ElogGroupData(db.Model):

    __tablename__ = 'elog_group_data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    sort = db.Column(db.Integer)
    private = db.Column(db.Integer)

class ElogData(db.Model):

    __tablename__ = 'elog_data'

# 	entry_id	title	author	created	text	severity_id	beam_mode_id	parent_id	read_only	comment
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    severity = db.Column(db.Integer)
    beam_mode = db.column(db.Integer)
    parent = db.column(db.Integer)
    read_only = db.column(db.Integer)
    comment = db.column(db.Integer)

@app.route('/')
def meLog():
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True #remove for production servers
    app.run()

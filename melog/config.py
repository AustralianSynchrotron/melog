from melog import app
import json

json_data=open('melog/config.json')
data = json.load(json_data)
json_data.close()

username = data['dbuser']
password = data['password']
host = data['host']
db_name = data['database']

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (username,password,host,db_name)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host:port/db_name'
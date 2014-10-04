from melog import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
#db = SQLAlchemy(app)
#db.Model.metadata.reflect[db.engine]
from melog.database import db

class ElogGroupData(db.Model):

    __tablename__ = 'elog_group_data'

    group_id = db.Column(db.Integer, primary_key=True)
    group_title = db.Column(db.Text)
    sort = db.Column(db.Integer)
    private = db.Column(db.Integer)

class ElogData(db.Model):

    __tablename__ = 'elog_data'

#   entry_id    title   author  created text    severity_id beam_mode_id    parent_id   read_only   comment
    entry_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    created = db.Column(db.DateTime)
    text = db.Column(db.Text)
    severity_id = db.Column(db.Integer)
    beam_mode_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    read_only = db.Column(db.Integer)
    comment = db.Column(db.Integer)
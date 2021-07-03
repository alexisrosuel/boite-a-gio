from database import db




class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    date_added = db.Column(db.DateTime(), unique=False, nullable=False, default=db.func.current_timestamp())
    nb_lecture = db.Column(db.Integer(), unique=False, nullable=False, default=0)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    user = db.Column(db.String(80), unique=False, nullable=False)
    #runtime = db.Column(db.Interval(), unique=True, nullable=False)

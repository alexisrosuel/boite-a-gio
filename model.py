from database import db




class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    date_added = db.Column(db.DateTime(), unique=False, nullable=False, default=db.func.current_timestamp())
    nb_lecture = db.Column(db.Integer(), unique=False, nullable=False, default=0)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    user = db.Column(db.String(80), unique=False, nullable=False)
    #runtime = db.Column(db.Interval(), unique=True, nullable=False)
    file = db.Column(db.LargeBinary, unique=False, nullable=False)
    transcription = db.Column(db.String(1000), unique=False, nullable=True)
    user_id = db.Column(db.String(80), unique=False, nullable=False)






class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False)







from wtforms import Form, StringField, SelectField
class SearchForm(Form):
    choices = []
    #select = SelectField('Rechercher :')
    search = StringField('')




class SortForm(Form):
    choices = ['Utilisateur', 'Nombre de lectures', 'Nom', 'Date d\'ajout']
    select = SelectField('', choices=choices)
    #name    = StringField(u'Full Name', [validators.required(), validators.length(max=10)])
    #address = TextAreaField(u'Mailing Address', [validators.optional(), validators.length(max=200)])

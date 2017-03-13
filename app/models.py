from . import db
import datetime

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    gender = db.Column(db.String(5))
    created = db.Column(db.DateTime, default=datetime.datetime.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __init__(self, fname=None, lname=None, age=None, bio=None, picture=None, gender=None):
        self.firstname = fname
        self.lastname = lname
        self.age = age
        self.bio = bio
        self.picture = picture
        self.gender = gender

    def __repr__(self):
        return '<User %r>' % (self.id)
        
    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'firstname': self.firstname,
           'lastname' : self.lastname,
           'image' : self.picture,
           'age' : self.age,
           'gender' : self.gender,
           'profile_created_on' : self.created,
       }
    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]

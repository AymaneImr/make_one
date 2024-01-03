from admin.extensions import db



'''
create a user database that stores his login information
'''
class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    #pets = db.relationship('Pet', backref='users')

#class Pet(db.Model):
    #_id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(14), nullable=False)
    #users_id = db.Column(db.Integer, db.ForeignKey('users._id'))

from enum import unique
from vadhyakalakshethra import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))



class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    usertype = db.Column(db.String(80))
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    qualification = db.Column(db.String(200))
    talents = db.Column(db.String(200))
    specialisation = db.Column(db.String(200))
    experience = db.Column(db.String(200))
    events = db.Column(db.String(200))
    achievements = db.Column(db.String(200))
    status= db.Column(db.String(200))
    type = db.Column(db.String(200))
    material = db.Column(db.String(200))
    price = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')

 





class Artist(db.Model):
    aid = db.Column(db.Integer,primary_key=True)
    aname = db.Column(db.String(200))
    aaddress = db.Column(db.String(200))
    qualification = db.Column(db.String(200))
    talents = db.Column(db.String(200))
    specialisation = db.Column(db.String(200))
    experience = db.Column(db.String(200))
    events = db.Column(db.String(200))
    achievements = db.Column(db.String(200))
    aemail = db.Column(db.String(200),unique=True)
    acontact = db.Column(db.String(200))
    password = db.Column(db.String(200))
    status= db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    email = db.Column(db.String(200),unique=True)
    contact = db.Column(db.String(200))
    password = db.Column(db.String(200))


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email= db.Column(db.String(200),unique=True)
    contact= db.Column(db.Integer)
    subject = db.Column(db.String(200))
    message= db.Column(db.String(200))
    usertype = db.Column(db.String(80), nullable=False)




class Vadhyam(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    type = db.Column(db.String(200))
    material = db.Column(db.String(200))
    price = db.Column(db.String(200))






class BookArtist(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(200))
    aid = db.Column(db.String(200))
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    aname = db.Column(db.String(200))
    aaddress = db.Column(db.String(200))
    aemail = db.Column(db.String(200))
    acontact = db.Column(db.String(200))
    bookdate=db.Column(db.String(200))
    booktime=db.Column(db.String(200))
    bookfor=db.Column(db.String(200))
    venue=db.Column(db.String(200))
    # status=db.Column(db.String(200))



class Order(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(200))
    name = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    type = db.Column(db.String(200))
    material = db.Column(db.String(200))
    price = db.Column(db.String(200))
    uname = db.Column(db.String(200))
    uaddress = db.Column(db.String(200))
    uemail = db.Column(db.String(200))
    ucontact = db.Column(db.String(200))




class Payment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.String(200))
    type = db.Column(db.String(200))
    material = db.Column(db.String(200))
    price = db.Column(db.String(200))
    uname = db.Column(db.String(200))
    uaddress = db.Column(db.String(200))
    uemail = db.Column(db.String(200))
    ucontact = db.Column(db.String(200))
    cardno= db.Column(db.String(200))
    expmonth= db.Column(db.String(200))
    expyear= db.Column(db.String(200))
    cvc= db.Column(db.String(200))
    

    
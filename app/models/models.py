import enum
from datetime import datetime
from flask_login import UserMixin
from app.views import db


class Status(enum.Enum):
    Done = "complete"
    Pending = "pending"
    Planning = "planning"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10))
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucket_list = db.relationship('BucketList', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User %r>" % self.username


class BucketList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    interests = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic')

    def __repr__(self):
        return "<Bucketlist %r>" % self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(120))
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.Enum(Status))
    date_accomplished = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucket_list = db.Column(db.Integer, db.ForeignKey('bucketlist.id'), nullable=False)
    photos = db.relationship('ItemPhotos', backref='item', lazy='dynamic')

    def __repr__(self):
        return "<Items %r>" % self.name


class ItemPhotos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)

    def __repr__(self):
        return "<Item Photos %r>" % self.id


class ProfilePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'))

    def __repr__(self):
        return "<Profile Photo %r>" % self.id


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), unique=True)
    caption = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolen, default=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return "<Photo %r>" % self.id

from db import db
from datetime import datetime

class Iteration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    stories = db.relationship('Story', backref='iteration', lazy=True)

class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date)
    stories = db.relationship('Story', backref='release', lazy=True)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')
    points = db.Column(db.Integer, default=0)
    iteration_id = db.Column(db.Integer, db.ForeignKey('iteration.id'), nullable=True)
    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')
    severity = db.Column(db.String(50), default='medium')
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    story = db.relationship('Story', backref=db.backref('bugs', lazy=True))

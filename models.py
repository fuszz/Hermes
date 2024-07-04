from main import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime
from cryptography.fernet import Fernet

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def encrypt_message(self, message, key):
        f = Fernet(key)
        return f.encrypt(message.encode())

    def decrypt_message(self, encrypted_message, key):
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()

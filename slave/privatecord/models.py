from datetime import datetime
import logging
import uuid

from dateutil.parser import parse

# local
from privatecord import db, CONFIG


def is_date(string: str) -> bool:
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False


def get_user_clubs_IDs(user_masterID: str, user_masterIP: str) -> list:
    user = User.query.filter_by(masterID=user_masterID, masterIP=user_masterIP).first()
    club_IDs: list = []
    if user:
        ucs = UsersClubs.query.filter_by(userID=user.id).all()
        club_IDs = [uc.serverIP for uc in ucs]
    return club_IDs


def get_user_clubs(user_masterID: str, user_masterIP: str) -> list:
    club_IDs: list = get_user_clubs_IDs(user_masterID, user_masterIP)
    club_list: list = []
    if len(club_IDs):
        club_list = Club.query.filter(Club.id.in_(club_IDs)).all()
    return club_list


def get_channel_messages(channel_id: str, date_from: str, date_to: str) -> list:
    messages = []    
    if not is_date(date_from) or not is_date(date_to):
        return messages
    # Limit date to config var
    datetime_from = parse(date_from, fuzzy=False)
    config_date = parse(CONFIG['SETTINGS']['message_max_date'], fuzzy=False)
    if datetime_from > config_date:
        date_from = CONFIG['SETTINGS']['message_max_date']
    # Find all messages linked to a channel ID
    messages = db.session.query(Message).filter(Message.datetime.between(date_from, date_to)).filter_by(channelID=channel_id).all()
    logging.info(f"Requested messages ({channel_id}, <{date_from}, {date_to}>). Returned {len(messages)} message(s).")
    # Return dictionary of messages
    return [msg.serialize_to_json() for msg in messages]


def generate_channel_ID() -> str:
    channelID: str = ''
    IDCanBeUsed: bool = False
    # Make sure ID does not exists in the database (very very small chance but it can happen)
    while not IDCanBeUsed:
        # Generate new ID
        channelID = str(uuid.uuid4())
        # Search the db
        if Channel.query.filter_by(id=channelID).first() is None:
            IDCanBeUsed = True
    return channelID

#----------------------------------------------------------------------------#
# SQLAlchemy Models
#----------------------------------------------------------------------------#

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    masterID = db.Column(db.String(36)) # UUID4 from Master Server
    masterIP = db.Column(db.String(15)) # IP of Master Server
    username = db.Column(db.String)
    avatarPath = db.Column(db.String)
    isBot = db.Column(db.Boolean)
    isSystem = db.Column(db.Boolean)

    clubs = db.relationship('UsersClubs', backref='user', lazy=True)

    def __repr__(self):
        return '[User] (' + str(self.id) +  ')'


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(36), nullable=False, unique=True) # UUID4
    systemChannelID = db.Column(db.Integer, nullable=False)
    afkChannelID = db.Column(db.Integer, nullable=False)
    rulesChannelID = db.Column(db.Integer, nullable=False)
    ownerID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    iconPath = db.Column(db.String(255), nullable=False)
    afkTimeout = db.Column(db.Integer, default=600)
    maxMembers = db.Column(db.Integer, default=-1)
    permissions = db.Column(db.Text, default='{}')
    roles = db.Column(db.Text, default='{}')

    channels = db.relationship('Channel', backref='club', lazy=True)
    users = db.relationship('UsersClubs', backref='club', lazy=True)

    def __repr__(self):
        return '[Club] (' + str(self.id) +  ')'


class Channel(db.Model):
    id = db.Column(db.String(36), primary_key=True) # UUID4
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '[Channel] (' + str(self.id) +  ')'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    channelID = db.Column(db.String(36), nullable=False)
    masterIP = db.Column(db.String(15), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Integer, nullable=False, default=0)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    responseToMessageID = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'[Message] ({str(self.id)}, {(self.userID)}, {self.channelID}, {self.masterIP}, {self.content}, {self.type}, {self.datetime}, {self.responseToMessageID})'

    def serialize_to_json(self):
        return {
            'id': self.id,
            'userID': self.userID,
            'channelID': self.channelID,
            'masterIP': self.masterIP,
            'content': self.content,
            'type': self.type,
            'datetime': self.datetime,
            'responseToMessageID':  self.responseToMessageID,
        }


class UsersClubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
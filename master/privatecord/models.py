import uuid

from flask_login import UserMixin

from privatecord import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return MasterUser.query.get(str(user_id))


def generate_user_ID() -> str:
    userID: str = ''
    IDCanBeUsed: bool = False
    # Make sure ID does not exists in the database (very very small chance but it can happen)
    while not IDCanBeUsed:
        # Generate new ID
        userID = str(uuid.uuid4())
        # Search the db
        if MasterUser.query.filter_by(id=userID).first() is None:
            IDCanBeUsed = True

    return userID

#----------------------------------------------------------------------------#
# SQLAlchemy Models
#----------------------------------------------------------------------------#

class MasterUser(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True) # UUID4
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    avatarFile = db.Column(db.String(20), nullable=False, default='default.jpg')
    isBot = db.Column(db.Boolean, default=False)
    isSystem = db.Column(db.Boolean, default=False)
    locale = db.Column(db.String(10), default='en')

    servers = db.relationship('MasterUsersServers', backref='masterUser', lazy=True)

    def __repr__(self):
        return f'[User] ( {self.id}, {self.username}, {self.email}, {self.avatarFile}, {self.isBot}, {self.isSystem})'


class SlaveServer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serverIP = db.Column(db.String(15), unique=True, nullable=False) # 255.255.255.255
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    users = db.relationship('MasterUsersServers', backref='slaveServer', lazy=True)

    def __repr__(self):
        return f'[SlaveServer] ( {self.id}, {self.serverIP}, {self.name}, {self.description})'


class MasterUsersServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    masterUserID = db.Column(db.String(36), db.ForeignKey('master_user.id'), nullable=False)
    slaveServerID = db.Column(db.Integer, db.ForeignKey('slave_server.id'), nullable=False)
    note = db.Column(db.String(255), nullable=True)
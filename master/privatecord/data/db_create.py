import logging

from privatecord import db
# from master.app import GenerateUserID, MasterUser, SlaveServer, MasterUsersServers

db.drop_all()
# Create the database and the db tables
db.create_all()

logging.warning('Dropped all tables and recreated the database.')

# user1 = MasterUser(GenerateUserID, 'admin', 'admin@admin.com', '1@qwerty')
# db.session.add(user1)
# user2 = MasterUser(GenerateUserID, 'user', 'user@mail.com', '1@qwerty')
# db.session.add(user2)

# db.session.commit()
# logging.info('Added 2 dummy accounts.')
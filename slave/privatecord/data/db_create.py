from master.app import db

# create the database and the db table
db.create_all()



db.session.commit()
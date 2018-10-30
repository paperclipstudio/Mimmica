import sqlite3
from App.Mimmica_User import User

db = 'Users.db'


def create_database(name=db):
    try:
        connection = sqlite3.connect(name)
        print(name + ' database created')
        connection.close()
    except:
        print("Database creation failed.")

    try:
        connection = sqlite3.connect(name)
        connection.execute("""CREATE TABLE users (
                                name text,
                                passwrd text,
                                bio text
                                )""")
        connection.commit()
        print('table created.')
        return connection
    except:
        print('creating table failed.')



def connect_to_db(database_name = db):
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except:
        print('failed to connect to database.')

def add_user(new_user:User, curser):
    curser.execute("INSERT INTO users VALUES (:name, :passwrd, :bio)", {'name':new_user.name,
                                                                         'passwrd':new_user.get_password(),
                                                                         'bio':new_user.get_bio()
                                                                         })
    curser.commit()






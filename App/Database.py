import sqlite3
from App.Mimmica_User import User
from App.Mimmica_Audio import Audio

db = 'Users.db'


def create_database(database_name=db):
    try:
        connection = sqlite3.connect(database_name)
        print(database_name + ' database created')
        connection.close()
    except:
        print("Database creation failed.")

    try:
        connection = sqlite3.connect(database_name)
        connection.execute("""CREATE TABLE users (
                                ID  INTEGER PRIMARY KEY,
                                name text,
                                passwrd text,
                                bio text
                                )""")
        connection.commit()
        print('User table created.')
    except:
        print('Creating user table failed.')

    try:
        connection = sqlite3.connect(database_name)
        connection.execute("""CREATE TABLE audio (
                                ID  INTEGER PRIMARY KEY,
                                user_name text,
                                file_name text,
                                created date 
                                )""")
        connection.commit()
        print('Audio table created.')
    except:
        print('Creating Audio table failed.')

    return connection


def connect_to_db(database_name = db):
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except:
        print('failed to connect to database.')

def add_user(new_user:User, cursor):
    #TODO make unique username
    cursor.execute("INSERT INTO users VALUES (NULL, :name, :passwrd, :bio)", {
                                                                         'name':new_user.name,
                                                                         'passwrd':new_user.get_password(),
                                                                         'bio':new_user.get_bio()
                                                                         })
    cursor.commit()

def remove_user(user_name:str, connection):
    cursor = connection.cursor()
    print("remove " + user_name)
    cursor.execute('''SELECT * FROM users WHERE name = ? ''', (user_name,))
    if not (cursor.fetchone()):
        print(user_name + ' not found')
        return
    cursor.execute('''DELETE FROM users WHERE name = ? ''', (user_name,))
    connection.commit()


def add_audio(new_audio,connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO audio VALUES (NULL, :file_name, :name, :created)", {
        'file_name': new_audio.file,
        'name': new_audio.creator,
        'created': new_audio.date
    })
    connection.commit()


def convert_to_audio_class(list):
    if list == None : return None
    return Audio(list[1],list[2],list[3])

def get_newest_audio(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audio ORDER by created")
    connection.commit()
    return convert_to_audio_class(cursor.fetchone())

def get_newest_by(users:User,connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audio WHERE user_name = ? ORDER by created", (users.name,))
    print('~~' + users.name)
    print_
    connection.commit()
    return convert_to_audio_class(cursor.fetchone())






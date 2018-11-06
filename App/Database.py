import os
import sqlite3
import pyaudio
from App.Mimmica_User import User
from App.Mimmica_Audio import Audio
import App.Mimmica_Recording as Recording

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
    except:
        print('Creating user table failed.')

    try:
        connection = sqlite3.connect(database_name)
        connection.execute("""CREATE TABLE audio (
                                ID  INTEGER PRIMARY KEY,
                                username text,
                                created date 
                                )""")
        connection.commit()
    except:
        print('Creating Audio table failed.')

    try:
        connection = sqlite3.connect(database_name)
        connection.execute("""CREATE TABLE following (
                                ID  INTEGER PRIMARY KEY,
                                username text,
                                following text,
                                since date 
                                )""")
        connection.commit()
    except:
        print('Creating Audio table failed.')
    return connection


def connect_to_db(database_name=db):
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except:
        print('failed to connect to database.')


class NoUserError(Exception):
    # TODO Add not a user exception when a user can't be found
    pass


def add_user(new_user: User, cursor):
    # TODO make unique username
    cursor.execute("INSERT INTO users VALUES (NULL, :name, :passwrd, :bio)", {
        'name': new_user.name,
        'passwrd': new_user.get_password(),
        'bio': new_user.get_bio()
    })
    cursor.commit()


def remove_user(user_name: str, connection):
    cursor = connection.cursor()
    print("remove " + user_name)
    cursor.execute('''SELECT * FROM users WHERE name = ? ''', (user_name,))
    if not (cursor.fetchone()):
        print(user_name + ' not found')
        return
    cursor.execute('''DELETE FROM users WHERE name = ? ''', (user_name,))
    connection.commit()


def add_audio_from_data(new_audio: [pyaudio.PyAudio], user: User, connection: sqlite3.connect) -> str:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO audio VALUES (NULL, ?, DATETIME())", (user.name,))

    connection.commit()


def print_table(connection: sqlite3.connect, table_name: str):
    cursor = connection.cursor()
    # TODO Make it so that table_name is parsed into execute
    cursor.execute("SELECT * FROM audio ")  # , (table_name,))
    table = cursor.fetchall()
    names = ''
    for column_name in cursor.description:
        names += column_name[0] + '   '
    print(names)
    for row in table:
        print('|' + '-' * len(str(row)))
        print('| ' + str(row))


def convert_to_audio_class(list):
    if not list:
        print("Convert to audio class was given none.")
        raise TypeError
        return None
    return Audio(str(list[0]) + '.wav', list[1], list[2])


def add_audio_to_table():
    pass


def reserve_audio_ID(connection: sqlite3.connect, user: User):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO audio VALUES(NULL, ? , DATETIME())", (user.name,))
    connection.commit()
    cursor.execute("SELECT ID FROM audio WHERE username = ? ORDER BY ID DESC", (user.name,))
    return cursor.fetchone()[0]


def get_newest_audio(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audio ORDER by created")
    return convert_to_audio_class(cursor.fetchone())


def get_newest_by(users: User, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM audio WHERE username = ?", (users.name,))
    connection.commit()
    return convert_to_audio_class(cursor.fetchone())


def add_follower(connection: sqlite3.connect, user: User, following):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO following VALUES (NULL, :user, :following, DATETIME() )", {
        'user': user.name,
        'following': following.name
    })

    connection.commit()


def remove_follow(connection: sqlite3.connect, user: User, following: User):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM following WHERE username = ? AND following = ?", (user.name, following.name))
    connection.commit()


def is_following(connection: sqlite3.connect, user: User, following: User) -> bool:
    cursor = connection.cursor()
    cursor.execute('''SELECT ID FROM following WHERE username = ? AND following = ?''', (user.name, following.name))

    if cursor.fetchone():
        return True
    else:
        return False


def save_audio_data_to_database(connection: sqlite3.connect, audio: [pyaudio.PyAudio], user: User,
                                filepath='../App/Audio/'):
    id = reserve_audio_ID(connection, user)
    Recording.SaveAudiotoWav(filepath, id, audio)
    # todo change to proper user method
    user._audio.append(id)

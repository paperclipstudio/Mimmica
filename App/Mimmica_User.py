
class User():
    ##TODO make paswords safer
    def __init__(self, name = None, password = None):
        if not (type(name) == str) or (len(name) > 15):
            raise NameError("Invalid name for new user")
        if not (type(password) == str or len(password > 25)):
            raise NameError("Invalid password for new user")#

        self.name = name
        self.__password = password
        self._audio = []
        self._friends = []
        self._bio = ''
        self.database_name = 'TestingDatabase'

    def __repr__(self):
        return self.name

    def set_bio(self, bio_line:str):
        if (type(bio_line) == str) and (len(bio_line) < 256):
            self._bio = bio_line
        else:
            raise TypeError

    def get_bio(self):
        return self._bio

    def __is_password_vaild(self, password:str):
        if password == self.__password:
            return True
        else:
            return False

    def set_password(self,current,new):
        if (self.__is_password_vaild(current)):
            self.__password = new
            return True
        else:
            print (self.name + ' Wrong password :(')
            return False

    def get_password(self):
        return self.__password

    def add_friends(self,new_friend):
        if isinstance(new_friend, str):
            self._friends.append(new_friend)
        else:
            print("username isn't a string")

    def record(self, path='../Audio/'):
        #todo User.Record
        pass


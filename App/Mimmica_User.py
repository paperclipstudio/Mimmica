class User():
    def __init__(self, name = None, password = None):
        if (not name):
            print("please enter name")
            return
        if not password:
            print("please enter password")
            return
        self.name = name
        self.__password = password
        self._audio = []
        self._friends = []
        self._bio = 'No bio yet :('

    def __str__(self):
        return self.name

    def set_bio(self, bio_line:str):
        self._bio = bio_line

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




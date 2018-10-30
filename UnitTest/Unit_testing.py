import unittest as test
import os

import App.Mimmica_User as user
import App.User_database as DB

class TestUserCreation(test.TestCase):
    def setUp(self):
        self.Tom = user.User('Tom', 'passw0rd')

    def test_normal_user(self):
        self.assertEqual(self.Tom.name, 'Tom')
        with self.assertRaises(AttributeError):
            print(self.Tom.__password)

        self.assertEqual(self.Tom._bio, 'No bio yet :(')
        self.Tom.set_bio('Hi my name is Tom, and i love music')
        self.assertEqual(self.Tom.get_bio(), ('Hi my name is Tom, and i love music'))
        self.assertFalse(self.Tom.set_password('bad_pasword', ' H@K£R N£T'))
        self.assertTrue(self.Tom.set_password('passw0rd', 'new_password'))
        self.Tom.add_friends('Tom')
        self.Tom.add_friends('some_one_else')
        self.Tom.add_friends(13434)
        self.assertTrue('Tom' in self.Tom._friends)
        self.assertTrue('some_one_else' in self.Tom._friends)
        self.assertFalse(13434 in self.Tom._friends)
        self.Tom.set_bio('Flime Slamp')


class TestDatabase(test.TestCase):
    def setUp(self):
        testdb = 'TestingDatabase'
        try:
            os.remove(testdb)
        except:
            pass
        self.rupert = user.User('Rupert', 'hello_world')
        self.george = user.User('George', 'hello_worlds')
        self.tom = user.User('Michel', 'dont hack me bro.')

        self.c = DB.create_database(testdb)
        DB.add_user(self.rupert, self.c)
        DB.add_user(self.george, self.c)

    def how_many_users(self, connection):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return len(users)

    def test_start(self):
        self.assertEqual(self.how_many_users(self.c), 2)

        DB.add_user(self.tom, self.c)
        self.assertEqual(self.how_many_users(self.c), 3)

    def test_large_sets(self):
        self.assertEqual(self.how_many_users(self.c),2)
        large_number = 1000
        for i in range(large_number):
            new_user = user.User('test', 'test')
            DB.add_user(new_user, self.c)
        self.assertEqual(self.how_many_users(self.c),large_number+2)

    def tearDown(self):
        self.c.close()


if __name__ == '__main__':
    test.main()


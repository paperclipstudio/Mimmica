import unittest as test

import os

import App.Mimmica_User as User
import App.Database as DataBase
import App.Mimmica_Audio as Audio
import App.Mimmica_Recording as Recording

class TestUserCreation(test.TestCase):
    def setUp(self):
        self.Tom = User.User('Tom', 'passw0rd')

    def test_normal_user(self):
        self.assertEqual(self.Tom.name, 'Tom')
        with self.assertRaises(AttributeError):
            print(self.Tom.__password)

        self.assertEqual(self.Tom._bio, '')
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


class TestUserDatabase(test.TestCase):
    def setUp(self):
        testdb = 'TestingDatabase'
        try:
            os.remove(testdb)
        except:
            pass
        self.c = DataBase.create_database(testdb)

        self.rupert = User.User('Rupert', 'hello_world')
        self.george = User.User('George', 'hello_worlds')
        self.tom = User.User('Michel', 'dont hack me bro.')

        self.audio1 = Audio.Audio('ice.wav', 'Rupert', '2017-02-10')
        self.audio2 = Audio.Audio('poker.wav', 'George', '2016-03-12')
        self.audio3 = Audio.Audio('sos.wav', 'Michel', '2014-06-16')
        self.audio4 = Audio.Audio('truck.wav', 'Rupert', '2011-02-21')

        audio_data = Recording.record()
        DataBase.add_audio_from_data(audio_data, self.tom, self.c)


        DataBase.add_user(self.rupert, self.c)
        DataBase.add_user(self.george, self.c)

    def how_many_users(self, connection):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return len(users)

    def test_start(self):
        self.assertEqual(self.how_many_users(self.c), 2)

        DataBase.add_user(self.tom, self.c)
        self.assertEqual(self.how_many_users(self.c), 3)

    def test_large_sets(self):
        self.assertEqual(2, self.how_many_users(self.c))
        large_number = 300
        for i in range(large_number):
            new_user = User.User('test', 'test')
            DataBase.add_user(new_user, self.c)
        self.assertEqual(self.how_many_users(self.c),large_number+2)


    def test_users_removal(self):
        self.assertEqual(2,self.how_many_users(self.c))
        DataBase.remove_user('George', self.c)
        self.assertEqual(1, self.how_many_users(self.c))
        DataBase.remove_user('Not a person', self.c)
        self.assertEqual(self.how_many_users(self.c), 1)
        DataBase.remove_user('Rupert', self.c)
        self.assertEqual(self.how_many_users(self.c), 0)
        DataBase.remove_user('Rupert', self.c)
        self.assertEqual(self.how_many_users(self.c), 0)

    def tearDown(self):
        self.c.close()

    # def test_add_audio(self):
    #     newest = DataBase.get_newest_audio(self.c)
    #     self.assertEqual('2017-02-10', newest.date)

    def test_reserve_audio_ID(self):
        DataBase.print_table(self.c, 'audio')
        self.assertEqual(2, DataBase.reserve_audio_ID(self.c, self.rupert))
        DataBase.print_table(self.c, 'audio')
        self.assertEqual(3, DataBase.reserve_audio_ID(self.c, self.george))

        self.assertEqual(4, DataBase.reserve_audio_ID(self.c, self.rupert))

    #
    # def test_audio_table_functions(self):
    #     DataBase.reserve_audio_ID(self.c, self.rupert)
    #     DataBase.reserve_audio_ID(self.c, self.rupert)
    #     DataBase.reserve_audio_ID(self.c, self.rupert)
    #     DataBase.reserve_audio_ID(self.c, self.rupert)
    #
    #     newest_by_george = DataBase.get_newest_by(self.george, self.c)
    #     self.assertEqual('2016-03-12', newest_by_george.date)
    #


    def test_new_following(self):
        DataBase.add_follower(self.c, self.george, self.rupert)
        self.assertTrue(DataBase.is_following(self.c, self.george, self.rupert))
        self.assertFalse(DataBase.is_following(self.c, self.rupert, self.george))

        DataBase.remove_follow(self.c, self.george, self.rupert)
        self.assertFalse(DataBase.is_following(self.c, self.george, self.rupert))

    def test_record_from_user_class(self):
        userA = User.User('Tom', 'testing')
        audio_data = userA.record()
        self.assertTrue(os.path.exists('../Audio/test/001.wav'))
        DataBase.add_audio_from_data(audio_data, userA, self.c)
        self.assertTrue(os.path.exists('../Audio/test/002.wav'))



class test_audio_class(test.TestCase):
    def test_errors(self):
        audioA = Audio.Audio('somefile.wav', 'Someuser', '2017-02-23')
        with self.assertRaises(TypeError):
            bad_audio = Audio.Audio('otherfile.wav', '', '1970-01-01')
            bad_audio = Audio.Audio('otherfile.wav', 'someone', '1930-12-25')
            bad_audio = Audio.Audio('', 'someone', '1970-01-01')



class test_audio_recording(test.TestCase):
    def setUp(self):
        try:
            os.remove('../Audio/test/001.wav')
        except:
            pass
        os.open('../Audio/test/001.wav',os.O_RDWR|os.O_CREAT )

    def test_creation(self):
        audio_test = Recording.record()
        Recording.SaveAudiotoWav('Audio/test/', '001.wav', audio_test)

        self.assertTrue(os.path.exists('../Audio/test/001.wav'))
        my_audio = Audio.Audio('test/001.wav', 'George', '1970-01-01')
        my_audio.play()
        print('audio should have played back')



    def test_data_recording_functions(self):
        #todo this
        pass


    def tearDown(self):
        try:
            pass
        except:
            print('test path never created')

if __name__ == '__main__':
    test.main()


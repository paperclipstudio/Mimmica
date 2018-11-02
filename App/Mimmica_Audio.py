import winsound

class Audio():
    def __init__(self, file=None, creator=None, date=None):
        if file==None:
            print('No attached file.')

        if creator==None:
            print('No creator')
            raise TypeError

        if date==None:
            print('No attached date.')
            raise TypeError

        self.file = file
        self.creator = creator
        self.date = date

    def play(self):
        winsound.PlaySound('../Audio/' +  self.file, winsound.SND_FILENAME)

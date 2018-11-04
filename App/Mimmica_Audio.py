import winsound

class Audio():
    def __init__(self, file=None, creator=None, date=None):
        if not file:
            print('No attached file.')
            raise TypeError

        if not creator:
            print('No creator')
            raise TypeError

        if not date:
            print('No attached date.')
            raise TypeError

        self.file = file
        self.creator = creator
        self.date = date

    def __repr__(self):
        return self.file + " by " + self.creator + ' on ' + self.date +'.'

    def play(self):
        winsound.PlaySound('../Audio/' +  self.file, winsound.SND_FILENAME)

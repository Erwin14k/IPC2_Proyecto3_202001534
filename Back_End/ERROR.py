class ERROR:
    def __init__(self,date,type):
        self.date=date
        self.type=type

    def dump(self):
        return {
            'date': self.date,
            'type': self.type,
        }
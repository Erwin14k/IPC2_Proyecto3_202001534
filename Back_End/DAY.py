class DAY:
    def __init__(self,date):
        self.date=date

    def dump(self):
        return {
            'date': self.date,
        }
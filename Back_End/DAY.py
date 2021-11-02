class DAY:
    def __init__(self,date,value,total):
        self.date=date
        self.value=value
        self.total=total

    def dump(self):
        return {
            'date': self.date,
        }
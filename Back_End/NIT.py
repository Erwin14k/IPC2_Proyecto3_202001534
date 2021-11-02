class NIT:
    def __init__(self,code,date,recieved_nit,emmited_nit):
        self.code=code
        self.date=date
        self.recieved_nit=recieved_nit
        self.emmited_nit=emmited_nit

    def dump(self):
        return {
            'code':self.code,
            'date': self.date,
            'recieved_nit':self.recieved_nit,
            'emmited_nit':self.emmited_nit,
        }
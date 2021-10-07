class DTE:
    def __init__(self,id_reference,emmiter_nit,reciever_nit,date,value,tax,total):
        self.id_reference=id_reference
        self.emmiter_nit=emmiter_nit
        self.reciever_nit=reciever_nit
        self.date=date
        self.value=value
        self.tax=tax
        self.total=total

    def dump(self):
        return {
            'id_reference': self.id_reference,
            'emmiter_nit': self.emmiter_nit,
            'reciever_nit':  self.reciever_nit,
            'date': self.date,
            'value': self.value,
            'tax':self.tax,
            'total':self.total,
        }
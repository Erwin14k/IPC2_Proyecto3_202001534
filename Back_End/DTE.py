class DTE:
    def __init__(self,code,id_reference,emmiter_nit,reciever_nit,date,value,tax,total,state):
        self.code=code
        self.id_reference=id_reference
        self.emmiter_nit=emmiter_nit
        self.reciever_nit=reciever_nit
        self.date=date
        self.value=value
        self.tax=tax
        self.total=total
        self.state=state

    def dump(self):
        return {
            'code': self.code,
            'id_reference': self.id_reference,
            'emmiter_nit': self.emmiter_nit,
            'reciever_nit':  self.reciever_nit,
            'date': self.date,
            'value': self.value,
            'tax':self.tax,
            'total':self.total,
            'state':self.state,
        }
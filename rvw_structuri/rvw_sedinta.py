import json
import os
import time
import uuid

import rvw_fisiere

from rvw_structuri import stringToDate, sedinta_a_trecut, calc_date_diff_now, datetime


class Sedinta:
    def __init__(self, initiator, desc, data_ora, ore_lucru, max_pers=50, data_initiere=None, participanti=[], prezenti=[], uid=None):
        if uid is None:
            self.uid = str(uuid.uuid4())
        else:
            self.uid = uid
        self.initiator = initiator
        self.desc = desc
        self.max_pers = max_pers
        self.data_ora = data_ora
        self.ore_lucru = ore_lucru
        if data_initiere is None:
            self.data_initiere = time.time()
        else:
            self.data_initiere = data_initiere
        self.participanti = participanti
        self.prezenti = prezenti

    def to_json(self):
        return json.dumps(self.__dict__)

    def save(self):
        with open(rvw_fisiere.getStructuriPath("sedinte",None)+self.uid+'.json', 'w', encoding='utf-8') as outfile:
                json.dump(self.__dict__, outfile, indent=4)

    @classmethod
    def getFiles(cls):
        li = [pers.replace(".json","") for pers in os.listdir(rvw_fisiere.getStructuriPath("sedinte",None))]
        return li

    @classmethod
    def getSedinta_acum(cls):
        sedinte = [cls.from_id(sid) for sid in cls.getFiles()]
        for sedinta in sedinte:
            dat = stringToDate(sedinta.data_ora)
            acum = datetime.now()
            if dat.day == acum.day and dat.month == acum.month and dat.year == acum.year:
                if acum.hour >= dat.hour and acum.hour <= dat.hour+sedinta.ore_lucru:
                    return sedinta
        return None

    @classmethod
    def get_raw(cls,id):
        try:
            with open(rvw_fisiere.getStructuriPath("sedinte",None)+id+'.json', 'r', encoding='utf-8') as fisier:
                return fisier.read()
        except:
            return None

    @classmethod
    def from_id(cls,id):
        try:
            with open(rvw_fisiere.getStructuriPath("sedinte",None)+id+'.json', 'r', encoding='utf-8') as fisier:
                return cls.from_json(fisier.read())
        except:
            return None

    @classmethod
    def from_json(cls, json_str):
        try:
            json_dict = json.loads(json_str)
            return cls(**json_dict)
        except:
            return None
        
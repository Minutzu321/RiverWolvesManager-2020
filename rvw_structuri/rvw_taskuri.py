import json
import os
import time
import uuid

import rvw_fisiere

taskstatus = ["In derulare","Terminat","Anulat"]

class Task:
    def __init__(self, initiator, nume, desc, termen, status=0, progres=0, data_initiere=None, participanti=[], uid=None, refuzati=[]):
        if uid is None:
            self.uid = str(uuid.uuid4())
        else:
            self.uid = uid
        self.initiator = initiator
        self.nume = nume
        self.desc = desc
        self.termen = termen
        self.status = status
        self.progres = progres
        if data_initiere is None:
            self.data_initiere = time.time()
        else:
            self.data_initiere = data_initiere
        self.participanti = participanti
        self.refuzati = refuzati

    def to_json(self):
        return json.dumps(self.__dict__)

    def save(self):
        with open(rvw_fisiere.getStructuriPath("taskuri",None)+self.uid+'.json', 'w', encoding='utf-8') as outfile:
                json.dump(self.__dict__, outfile, indent=4)

    @classmethod
    def getFiles(cls):
        li = [pers.replace(".json","") for pers in os.listdir(rvw_fisiere.getStructuriPath("taskuri",None))]
        return li

    @classmethod
    def get_raw(cls,id):
        try:
            with open(rvw_fisiere.getStructuriPath("taskuri",None)+id+'.json', 'r', encoding='utf-8') as fisier:
                return fisier.read()
        except:
            return None

    @classmethod
    def get_show(cls,id):
        num = len(cls.from_id(id).participanti)
        try:
            with open(rvw_fisiere.getStructuriPath("taskuri",None)+id+'.json', 'r', encoding='utf-8') as fisier:
                return fisier.read().replace("rvw_participanti",str(num))
        except:
            return None

    @classmethod
    def from_id(cls,id):
        try:
            with open(rvw_fisiere.getStructuriPath("taskuri",None)+id+'.json', 'r', encoding='utf-8') as fisier:
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
        
import json
import logging
import uuid
import time
import rvw_fisiere
import rvw_structuri
import os
from difflib import SequenceMatcher


class Persoana:
    def __init__(self, uid=None, nume="unk", encodings=[], infos=[], interes=0):
        if uid is None:
            self.uid = str(uuid.uuid4())
        else:
            self.uid = uid
        self.nume = nume
        self.encodings = encodings
        self.interes = interes
        self.infos = infos

    @classmethod
    def getCType(cls): return "persoana"

    def to_json(self):
        return json.dumps(self.__dict__)

    def save(self):
        with open(rvw_fisiere.getStructuriPath("persoane",self.getCType())+self.uid+'.json', 'w', encoding='utf-8') as outfile:
            global rvw_cache
            try:
                if rvw_cache: pass
                for cached in rvw_cache:
                    if cached[0] == self.uid:
                        cached[1] = json.dumps(self.__dict__)
                        # print("SALVAT IN CACHE")
            except: pass
            json.dump(self.__dict__, outfile, indent=4)

    # def addPoza(self, nume_poza, imagine, enc):
    #     path = rvw_fisiere.getStructuriPath("persoane/poze",self.uid)
    #     ctr = nume_poza
    #     i=0
    #     while ctr+'.png' in os.listdir(): 
    #         i+=1
    #         ctr = nume_poza+"-"+str(i)
    #     imagine.save(path+ctr+".png")
    #     with open(path+ctr+'.json', 'w', encoding='utf-8') as outfile:
    #         ob = {encodings: enc}
    #         json.dump(ob, outfile, indent=2)

    

    @classmethod
    def getFiles(cls):
        li = [pers.replace(".json","") for pers in os.listdir(rvw_fisiere.getStructuriPath("persoane",cls.getCType()))]
        return li


    @classmethod
    def getRaw(cls,uid):
        p = rvw_fisiere.getStructuriPath("persoane",cls.getCType())+uid+'.json'
        if os.path.isfile(p):
            with open(p, 'r', encoding='utf-8') as fisier:
                rez = fisier.read()
                return rez
            

    @classmethod
    def getByEnc(cls,enc):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if enc in content:
                pers = cls.from_json(content)
                if enc in pers.encodings:
                    return pers
        return None

    @classmethod
    def getByPoza(cls,poza):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if poza in content:
                return cls.from_json(content)
        return None

    @classmethod
    def getByNume(cls,nume):
        if nume == 'unk': return None
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if nume in content:
                pers = cls.from_json(content)
                if pers.nume == nume:
                    return pers
        return None

    @classmethod
    def from_id(cls,id):
        try:
            with open(rvw_fisiere.getStructuriPath("persoane",cls.getCType())+id+'.json', 'r', encoding='utf-8') as fisier:
                return cls.from_json(fisier.read())
        except:
            return None

    @classmethod
    def from_json(cls, json_str):
        try:
            json_dict = json.loads(json_str)
            return cls(**json_dict)
        except Exception as e:
            logging.error(str(e))
            return None



#Clasa pentru Playeri
class Rezervare(Persoana):
    def __init__(self, uid=None, nume="unk", encodings=[], infos=[], cod=None, telefon=None, persoane=1, ips=[], interes=50, data_inregistrare=None, status="pending"):
        Persoana.__init__(self, uid, nume, encodings, infos, interes)
        if cod is None:
            self.cod = str(uuid.uuid4())
        else:
            self.cod = cod
        self.telefon = telefon
        self.ips = ips
        self.persoane = persoane
        if data_inregistrare is None:
            self.data_inregistrare = time.time()
        else:
            self.data_inregistrare = data_inregistrare
        self.status = status

    @classmethod
    def getCType(cls): return "rezervare"

    @classmethod
    def getByCod(cls,cod):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if cod in content:
                player = cls.from_json(content)
                if player.cod == cod:
                    return player
        return None

    @classmethod
    def getByTelefon(cls,tel):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if tel in content:
                pers = cls.from_json(content)
                if pers.telefon == tel:
                    return pers
        return None
    
    @classmethod
    def getByIP(cls,ip):
        pers = []
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if ip in content:
                mem = cls.from_json(content)
                if mem and ip in mem.ips:
                    logging.info("added"+content)
                    pers.append(mem)
        return pers




#Clasa pentru Playeri
class Player(Persoana):
    def __init__(self, uid=None, nume="unk", encodings=[], infos=[], interes=50, cod=None, indicii=[], ips=[], data_inregistrare=None, telefon=None, platit=0, provocari = [], poze = [], indiciu_curent=None, provocare_curenta=None, persoane=0, dif=1, pickup=0, relax=False, copii=False, adolescenti=False, adulti=False, semnatura = None, locatie = None, puncte = 0):
        Persoana.__init__(self, uid, nume, encodings, infos, interes)
        if cod is None:
            self.cod = str(uuid.uuid4())
        else:
            self.cod = cod
        self.indicii = indicii
        self.indiciu_curent = indiciu_curent
        self.ips = ips
        self.telefon = telefon
        if data_inregistrare is None:
            self.data_inregistrare = time.time()
        else:
            self.data_inregistrare = data_inregistrare
        self.platit = platit
        self.provocari = provocari
        self.provocare_curenta = provocare_curenta
        self.poze = poze
        self.persoane = persoane
        self.dif = dif
        self.pickup = pickup
        self.relax = relax
        self.copii = copii
        self.adolescenti = adolescenti
        self.adulti = adulti
        self.semnatura = semnatura
        self.locatie = locatie
        self.puncte = puncte


    @classmethod
    def getCType(cls): return "player"


    @classmethod
    def getByIndiciu(cls,indiciu):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if indiciu in content:
                player = cls.from_json(content)
                if player.indiciu_curent == indiciu:
                    return player
        return None

    @classmethod
    def getByCod(cls,cod):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if cod in content:
                player = cls.from_json(content)
                if player.cod == cod:
                    return player
        return None

    @classmethod
    def getByEmail(cls,email):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if email in content:
                pers = cls.from_json(content)
                if pers.email == email:
                    return pers
        return None
    
    @classmethod
    def getByIP(cls,ip):
        pers = []
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if ip in content:
                mem = cls.from_json(content)
                if ip in mem.ips:
                    pers.append(mem)
        return pers









#Clsasa pentru membri
class Membru(Persoana):
    def __init__(self, uid=None, nume=None, encodings=[], infos=[], loguid=None, interese=[], prezente=[], rapoarte=[], interes=100, istoric=[], incredere=0, seccodes=[], ips=[], email=None, telefon=None, data_nastere=None, rol=None, qr=None, locatii=[], status="pending", porecla=None, comprehensiuni=[], data_inregistrare=None, descriere=""):
        Persoana.__init__(self, uid, nume, encodings, infos, 100)
        self.email = email
        self.telefon = telefon
        self.ips = ips
        if data_inregistrare is None:
            self.data_inregistrare = time.time()
        else:
            self.data_inregistrare = data_inregistrare
        self.data_nastere = data_nastere
        self.rol = rol
        if qr is None:
            self.qr = str(uuid.uuid4())
        else:
            self.qr = qr
        if loguid is None:
            self.loguid = str(uuid.uuid4())
        else:
            self.loguid = loguid
        self.locatii = locatii
        self.istoric = istoric
        self.incredere = incredere
        self.status = status
        self.seccodes = seccodes
        self.interese = interese
        self.prezente = prezente
        self.rapoarte = rapoarte
        self.porecla = porecla
        self.descriere = descriere
        self.comprehensiuni = comprehensiuni

    def getImportanta(self):
        bonus = 0
        if self.rol == "Voluntar":
            bonus = -10
            if self.interese:
                bonus = -9
        return (self.data_inregistrare**float(-1))*float(rvw_structuri.getRolByDisp(self.rol)[0]*20)+float(bonus)

    def getTasks(self):
        tasks = []
        for task_id in rvw_structuri.Task.getFiles():
            tsk = rvw_structuri.Task.from_id(task_id)
            if tsk and self.uid in tsk.participanti:
                tasks.append(task_id)
        return tasks
        
    @classmethod
    def getCType(cls): return "membru"

    @classmethod
    def getByLoguid(cls,loguid):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if loguid in content:
                pers = cls.from_json(content)
                if pers.loguid == loguid:
                    return pers
        return None

    @classmethod
    def getByEmail(cls,email):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if email in content:
                pers = cls.from_json(content)
                if pers.email == email:
                    return pers
        return None

    @classmethod
    def getByQR(cls,qr):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if qr in content:
                pers = cls.from_json(content)
                if pers.qr == qr:
                    return pers
        return None

    @classmethod
    def getByTelefon(cls,telefon):
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if telefon in content:
                pers = cls.from_json(content)
                if pers.telefon == telefon:
                    return pers
        return None

    @classmethod
    def getByPorecla(cls,porecla):
        porecla = porecla.lower()
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if porecla in content:
                pers = cls.from_json(content)
                if pers.porecla == porecla:
                    return pers
        return None

    @classmethod
    def getAccepted(cls):
        pers = []
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if "acceptat" in content:
                mem = cls.from_json(content)
                if mem.status == 'acceptat' and not "inactiv" in mem.infos:
                    pers.append(mem)
        return pers

    @classmethod
    def getByIP(cls,ip):
        pers = []
        for ident_id in cls.getFiles():
            content = cls.getRaw(ident_id)
            if ip in content:
                mem = cls.from_json(content)
                if ip in mem.ips:
                    pers.append(mem)
        return pers

    @classmethod
    def search(cls, skeys):
        returns = []
        for skey in skeys.lower().split(" "):
            for ident_id in cls.getFiles():
                mem = cls.from_id(ident_id)
                if "@" in skey:
                    if SequenceMatcher(None, mem.email, skey).ratio() >= 0.88:
                        returns.append(mem)
                        continue
                for num in mem.nume.replace("-"," ").replace("  "," ").split(" "):
                    if SequenceMatcher(None, num.lower(), skey).ratio() >= 0.88:
                        returns.append(mem)
                        break
                if SequenceMatcher(None, mem.rol.lower(), skey).ratio() >= 0.88:
                    returns.append(mem)
                    continue
                if mem.porecla and SequenceMatcher(None, mem.porecla, skey).ratio() >= 0.88:
                    returns.append(mem)
                    continue
                if skey.isdigit() and skey.startswith("07") and skey in mem.telefon:
                    returns.append(mem)
                    continue
                if skey in mem.data_nastere.replace(", 00:00:00", ""):
                    returns.append(mem)
                    continue
                for inter in mem.interese:
                    if skey.lower() in inter.lower():
                        returns.append(mem)
                        break
        return returns



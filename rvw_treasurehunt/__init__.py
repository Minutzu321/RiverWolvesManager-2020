import rvw_fisiere
import json
import os
import time
import uuid

def getIndicii():
    lista = [indiciu.replace(".json","") for indiciu in os.listdir(rvw_fisiere.getTHuntPath("indicii"))]
    return lista

def getIndiciu(indiciu,android):
    indiciu = indiciu.replace(".json","")
    if os.path.isfile(rvw_fisiere.getTHuntPath("indicii")+indiciu+".json"):
        file = open(rvw_fisiere.getTHuntPath("indicii")+indiciu+".json", 'r')
        data = file.read()
        file.close()
        data = json.loads(data)
        if android:
            data['poza'] = None
        data['uid'] = indiciu
        return data
    return None

def setPozaByPozaUUID(poza_uuid, poza_data):
    for indiciu in getIndicii():
        if os.path.isfile(rvw_fisiere.getTHuntPath("indicii")+indiciu+".json"):
            file = open(rvw_fisiere.getTHuntPath("indicii")+indiciu+".json", 'r')
            data = file.read()
            file.close()
            data = json.loads(data)
            if data['poza'] == poza_uuid:
                file = open(rvw_fisiere.getTHuntPath("indicii")+indiciu+".json", 'w')
                data['poza'] = poza_data
                json.dump(data, file, indent=4)
                file.close()
            

def getRandomUUID():
    uid = str(uuid.uuid4())
    if os.path.isfile(rvw_fisiere.getTHuntPath("indicii")+uid+".json"):
        return getRandomUUID()
    else:
        return uid

def addIndiciu(lat,lng,poza,acuratete,dificultate,intrebare,raspuns):
    data = {
        'lat': lat,
        'lng': lng,
        'poza': poza,
        'acuratete': acuratete,
        'dificultate': dificultate,
        'intrebare': intrebare,
        'raspuns': raspuns,
        'timp': time.time()
    }

    uidresp = getRandomUUID()
    file = open(rvw_fisiere.getTHuntPath("indicii")+uidresp+".json", 'w+')
    json.dump(data, file, indent=4)
    file.close()
    return uidresp

from .rvw_coords import getGraf, gaseste_drumurile
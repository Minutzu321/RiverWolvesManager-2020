import logging
from face_recognition.api import face_distance
import rvw_fisiere
import rvw_structuri
from rvw_creier import Informatie

import os
import json
import numpy as np
import face_recognition
from PIL import Image
from sklearn import neighbors
import numpy as np

cache_list = []
algo = None

def antreneaza():
    global algo
    X = []
    y = []
    algo = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm="ball_tree", weights='distance')
    for info_id in Informatie.getFiles():
        info = Informatie.from_id(info_id)
        for ped in info.pat:
            encs = getFaceData(ped)["encodings"]
            X.append(encs)
            y.append(info.uid)
    if len(X) > 0:
        algo.fit(X, y)
    else:
        logging.info("alg nu e antrenat")


def prezi(tencs):
    try:
        global algo
        if not algo:
            antreneaza()
        prezis = Informatie.from_id(algo.predict([tencs])[0])
        # print(prezis)
        dist_min = 1
        for ped in prezis.pat:
                encs = getFaceData(ped)["encodings"]
                d = face_recognition.face_distance([np.asarray(encs, dtype=np.float32)], np.asarray(tencs, dtype=np.float32))[0]
                if d<dist_min: dist_min = d
        if dist_min < .6:
            return (prezis, dist_min)
        else:
            return None
    except Exception as e:
        logging.info(e)
        return None
    
    
        



def addFaceToPers(pers, facefile):
    if rvw_structuri.isPersoana(pers):
        pers = rvw_structuri.Persoana.from_id(pers)
        if pers:
            pers.encodings.append(facefile)
            pers.save()
            return True
    elif rvw_structuri.isPlayer(pers):
        player = rvw_structuri.Player.from_id(pers)
        if player:
            player.encodings.append(facefile)
            player.save()
            return True
    elif rvw_structuri.isMembru(pers):
        mem = rvw_structuri.Membru.from_id(pers)
        if mem:
            mem.encodings.append(facefile)
            mem.save()
        return True
    return False

def getPath(nume,nr):
    if nr is None:
        return rvw_fisiere.getCreierPath("facerecog",nume)
    return rvw_fisiere.getCreierPath("facerecog/"+nume,str(nr))

def addFaceToFile(nume,nr,pilimg,encs,timestamp,lat,lng):
    global cache_list
    cache_list.append(nume)
    fpath = getPath(nume,nr)
    with open(fpath+'encodings.json', 'w', encoding='utf-8') as outfile:
                json.dump({
                    "encodings":encs.tolist(),
                    "timestamp":timestamp,
                    "lat":lat,
                    "lng":lng
                    }, outfile, indent=4)
    pilimg.save(fpath+'imagine.png')

def getFaceFiles():
    global cache_list
    if not cache_list:
        pth = rvw_fisiere.getCreierPath("facerecog",None)
        cache_list = os.listdir(pth)
    l = []
    for poza in cache_list:
        npth = rvw_fisiere.getCreierPath("facerecog",poza)
        subp = os.listdir(npth)
        for s in subp:
            l.append(poza+"/"+s)
    return l

def getFaceData(filepath):
    pth = rvw_fisiere.getCreierPath("facerecog",filepath)+'encodings.json'
    if os.path.exists(pth):
        with open(pth) as json_file:
            return json.load(json_file)
    else:
        ptz = rvw_fisiere.getCreierPath("facerecog",filepath)
        lista = os.listdir(ptz)
        try:
            if lista:
                for el in lista:
                    os.remove(ptz+el)
            os.rmdir(ptz)
        except Exception as err: print(err)
        return None

def clearCache():
    global cache_list
    del cache_list[:]

def photoInSystem(nume):
    global cache_list
    try:
        if not cache_list:
            pth = rvw_fisiere.getCreierPath("facerecog",None)
            cache_list = os.listdir(pth)
        return nume in cache_list
    except:
        cache_list = []
        return photoInSystem(nume)

def checkFaces(nume,poza,timestamp,lat,lng):
    pil = poza.convert('RGB')
    arrimg = np.array(pil)
    face_locs = face_recognition.face_locations(arrimg)
    if len(face_locs) == 0:
        getPath(nume,None)
        return 0
    face_encs = face_recognition.face_encodings(arrimg,face_locs)
    for i in range(len(face_locs)):
        top, right, bottom, left = face_locs[i]
        imagine_fata = Image.fromarray(arrimg[top:bottom, left:right])
        addFaceToFile(nume,i,imagine_fata,face_encs[i],timestamp,lat,lng)
    return len(face_locs)
        



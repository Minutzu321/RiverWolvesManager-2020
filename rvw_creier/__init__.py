import multiprocessing
import time
from .rvw_info import *
from .rvw_drive import *
from .rvw_person_matcher import *
from .rvw_facerecog import *
from configparser import ConfigParser
import os.path
from os import path
from datetime import datetime

def saveConf(config_object):
    with open('config.ini', 'w') as conf:
        config_object.write(conf)



def start():
    config_object = ConfigParser()
    if not path.exists("config.ini"):
        config_object["CREIER"] = {
            "drive_incep": str(time.time()),
            "person_incep": str(time.time())
        }
        saveConf(config_object)
    else:
        config_object.read("config.ini")

    

    # print("Face recog started")
    # s = time.time()
    # files = getFaceFiles()
    # for face in files:
    #     face = getFaceData(face)
    #     if face:
    #         if face['lng']: print(face)
    # e = time.time()
    # print(str(e-s))
    print("Creier process pornit")
    #scannerele faciale,temporale si geospatiale pentru drive
    driveThread = multiprocessing.Process(target=startDriveScan)
    #identificarea conexiunilor intre persoane
    personThread = multiprocessing.Process(target=startPersonMatcher)

    driveThread.start()
    personThread.start()

    conf = config_object["CREIER"]

    drive_incep = conf["drive_incep"]
    person_incep = conf["person_incep"]

    #fallback system
    while True:
        try:
            now = time.time()
            if not driveThread.is_alive() and now-float(drive_incep) >= 1800:
                driveThread = multiprocessing.Process(target=startDriveScan)
                driveThread.start()
                drive_incep = time.time()
                conf["drive_incep"] = str(drive_incep)
                saveConf(config_object)
            if not personThread.is_alive() and now-float(person_incep) >= 120:
                personThread = multiprocessing.Process(target=startPersonMatcher)
                personThread.start()

                person_incep = time.time()
                conf["person_incep"] = str(person_incep)
                saveConf(config_object)
        except Exception as err: 
            print(err)
        time.sleep(30)

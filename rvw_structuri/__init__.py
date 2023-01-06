from .rvw_persoana import *
from .rvw_roluri import *
from .rvw_data import *
from .rvw_locatie import *
from .rvw_taskuri import *
from .rvw_contact import *
from .rvw_interese import *
from .rvw_sedinta import *
import rvw_fisiere
import os

def isPersoana(uid):
    return Persoana.from_id(uid) is not None

def isPlayer(uid):
    return Player.from_id(uid) is not None

def isMembru(uid):
    return Membru.from_id(uid) is not None

def isBanned(ip):
    for uid in Membru.getFiles():
        raw = Membru.getRaw(uid)
        if ip in raw and "banat" in raw and Membru.from_id(uid).status == 'banat':
            return True
    for uid in Player.getFiles():
        raw = Player.getRaw(uid)
        if ip in raw and "banat" in raw and Player.from_id(uid).status == 'banat':
            return True
    return False

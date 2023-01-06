import os

rvw_root = "" # radacina trebuie sa aiba semnul "/" dupa ea

def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getLogsFile():
    return rvw_root+"loguri.log"

def getCreierPath(dire, loc):
    if loc is None:
        path = rvw_root+"fisiere/rvw_creier/"+dire+"/"
        createPath(path)
        return path
    else:
        path = rvw_root+"fisiere/rvw_creier/"+dire+"/"+loc+"/"
        createPath(path)
        return path

def getStructuriPath(dire, loc):
    path = rvw_root+"fisiere/rvw_structuri/"+dire+"/"
    if loc:
        path = rvw_root+"fisiere/rvw_structuri/"+dire+"/"+loc+"/"
    createPath(path)
    return path

def getWebFilesPath(fi):
    path = rvw_root+"fisiere/rvw_webfiles/"+fi
    createPath(path)
    return path

def getTHuntPath(fi):
    path = rvw_root+"fisiere/rvw_treasurehunt/"+fi+"/"
    createPath(path)
    return path



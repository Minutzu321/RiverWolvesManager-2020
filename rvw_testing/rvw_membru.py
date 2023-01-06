from rvw_structuri import *
def getMembriNumere():
    voluntari = 0
    alumni = 0
    mecanici = 0
    programatori = 0
    media = 0
    designeri = 0
    mentori = 0
    for mem in Membru.getAccepted():
        if getRolByDisp(mem.rol)[3] == 885:
            voluntari += 1
        if getRolByDisp(mem.rol)[3] == 218:
            media += 1
        if getRolByDisp(mem.rol)[3] == 937:
            mecanici += 1
        if getRolByDisp(mem.rol)[3] == 205:
            programatori += 1
        if getRolByDisp(mem.rol)[3] == 186:
            designeri += 1
        if getRolByDisp(mem.rol)[3] == 926:
            alumni += 1
        if getRolByDisp(mem.rol)[3] == 183:
            mentori += 1
    return [voluntari,alumni,mecanici,programatori,media,designeri,mentori]

getMembriNumere()
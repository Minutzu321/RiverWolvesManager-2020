from .event import RVWEvent
from flask import render_template
from rvw_structuri import Sedinta, Membru, stringToDate, calc_date_diff_now, sendNotif, Locatie

class RVWPrezent(RVWEvent):
    def __init__(self):
        RVWEvent.__init__(self, "prezent")
    def execute(self, argumente = []):
        sedinta = Sedinta.getSedinta_acum()
        if sedinta and argumente[2].uid not in sedinta.prezenti:
            lat = argumente[0]['rvw_lat']
            lon = argumente[0]['rvw_lon']
            acc = argumente[0]['rvw_acc']
            mem = argumente[2]
            mem.locatii.append(Locatie(lat,lon,acc).to_json())
            mem.save()
            sedinta.prezenti.append(mem.uid)
            sedinta.save()
            sendNotif("Prezenta",mem.nume+", Acc: "+str(acc))
            return "Prezenta a fost inregistrata"
        return "Nu participi la o sedinta"

class RVWPartikip_Sedinta(RVWEvent):
    def __init__(self):
        RVWEvent.__init__(self, "partikip_sedinta")

    def execute(self, argumente = []):
        seduid = argumente[0]['rvw_sedinta']
        mem = argumente[2]
        sedinta = Sedinta.from_id(seduid)
        if sedinta:
            if len(sedinta.participanti) >= sedinta.max_pers:
                return "Sedinta este plina!"
            if mem.uid not in sedinta.participanti:
                sedinta.participanti.append(mem.uid)
                sedinta.save()
                sendNotif("Inregistrare sedinta",mem.nume+", "+sedinta.data_ora)
                return "Ai fost inregistrat la sedinta!"
            else:
                return "Deja esti inregistrat la sedinta asta!"
        return "Sedinta nu exista."

class RVWNuPartikip_Sedinta(RVWEvent):
    def __init__(self):
        RVWEvent.__init__(self, "nupartikip_sedinta")

    def execute(self, argumente = []):
        seduid = argumente[0]['rvw_sedinta']
        mem = argumente[2]
        sedinta = Sedinta.from_id(seduid)
        if sedinta:
            if mem.uid in sedinta.participanti:
                sedinta.participanti.remove(mem.uid)
                sedinta.save()
                mem.infos.append(["anulare",sedinta.uid])
                mem.save()
                sendNotif("Anulare inregistrare sedinta",mem.nume+", "+sedinta.data_ora)
                return "Inregistrarea a fost anulata!"
            else:
                return "Nu esti inregistrat la sedinta asta!"
        return "Sedinta nu exista."
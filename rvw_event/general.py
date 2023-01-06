from .event import RVWEvent
from flask import render_template
from rvw_structuri import Sedinta, Membru, stringToDate, calc_date_diff_now, sendNotif, sedinta_a_trecut, getRolByDisp

class RVWGeneral(RVWEvent):
    def __init__(self):
        RVWEvent.__init__(self, "get_general")

    def getWeekDay(self, dat):
        if dat == 0:
            return "Luni"
        if dat == 1:
            return "Marti"
        if dat == 2:
            return "Miercuri"
        if dat == 3:
            return "Joi"
        if dat == 4:
            return "Vineri"
        if dat == 5:
            return "Sambata"
        if dat == 6:
            return "Duminica"

    def execute(self, argumente = []):
        final = ""

        #PREZENTA
        sed_acum = Sedinta.getSedinta_acum()
        if sed_acum and argumente[2].uid in sed_acum.participanti and argumente[2].uid not in sed_acum.prezenti:
            final += render_template("general/prezenta.html", seccode = argumente[1])

        # SEDINTE
        sedinte_ids = Sedinta.getFiles()
        sedinte = [Sedinta.from_id(sid) for sid in sedinte_ids]
        sedinte.sort(key=lambda x: stringToDate(x.data_ora), reverse=False)
        if len(sedinte_ids) > 0:
            content = ""
            for sedinta in sedinte:
                data_t = stringToDate(sedinta.data_ora)
                if sedinta_a_trecut(data_t):
                        continue
                dist = calc_date_diff_now(data_t)
                if dist < 0:
                    continue
                titlu = sedinta.data_ora.split(",")[0]

                if dist == 0:
                    titlu = "Azi"
                    titlu += " ("+self.getWeekDay(data_t.weekday())+")"
                if dist == 1:
                    titlu = "Maine"
                    titlu += " ("+self.getWeekDay(data_t.weekday())+")"
                if dist == 2:
                    titlu = "Poimaine"
                    titlu += " ("+self.getWeekDay(data_t.weekday())+")"
                elif dist > 2 and dist < 7:
                    titlu += " ("+self.getWeekDay(data_t.weekday())+")"
                elif dist >= 7:
                    titlu += " (in "+str(dist)+" zile)"

                ora_raw = sedinta.data_ora.split(" ")[1].split(":")
                ora = ora_raw[0]+":"+ora_raw[1]

                ore_len = sedinta.ore_lucru
                ore = str(ore_len)
                if ore_len == 1:
                    ore = "o ora"
                else:
                    ore += " ore"
                ore += "(pana la "+ str(int(ora_raw[0])+ore_len)+":"+ora_raw[1]+")"
                    
                participhtml = ""
                for puuid in sedinta.participanti:
                    membr_t = Membru.from_id(puuid)
                    participhtml += '''<a class="dropdown-item" href="javascript:;">'''+membr_t.nume+" - "+getRolByDisp(membr_t.rol)[2]+'''</a>'''

                
                status = 0
                if len(sedinta.participanti) >= sedinta.max_pers:
                    status = 2
                if argumente[2].uid in sedinta.participanti:
                    status = 1
                

                content += render_template("general/templ_sedinta.html", sedinta_uid = sedinta.uid,
                 titlu = titlu, descriere = sedinta.desc,
                  nr_part = str(len(sedinta.participanti)) + " din "+str(sedinta.max_pers),
                   ora = ora, ore = ore, status = status, participanti = participhtml)
            final += render_template("general/div_sedinte.html", content = content, seccode = argumente[1])


        return final



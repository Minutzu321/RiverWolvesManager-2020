from rvw_web import app, request, jsonify
import rvw_structuri
import rvw_template

import rvw_event

rvw_route_api_membri = "/rvw-api/membri/<uid>/"

@app.route("/rvw-api/event/execevent/<uid>/<event>", methods=['POST'])
def execute_event(uid, event):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            return rvw_event.execute(event, [request.form, uid, mem])
        return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."
    return "Invalid. Nu esti logat."


@app.route(rvw_route_api_membri+'prezent', methods=['POST'])
def submit_prezenta(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            lat = request.form['rvw_lat']
            lon = request.form['rvw_lon']
            acc = request.form['rvw_acc']
            mem.locatii.append(rvw_structuri.Locatie(lat,lon,acc).to_json())
            mem.save()
            rvw_structuri.sendNotif("Prezenta",mem.nume)
            return "Prezenta a fost inregistrata"
        return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."
    return "Invalid"

@app.route(rvw_route_api_membri+'partikip_task', methods=['POST'])
def partikip_task(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            task = rvw_structuri.Task.from_id(request.form['rvw_task'])
            if mem.uid not in task.participanti:
                task.participanti.append(mem.uid)
                task.save()
                rvw_structuri.sendNotif("Task",mem.nume+" participa la taskul "+task.nume)
                return "Ai fost repartizat"
            else:
                return "Deja participi la task"
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'edit_task', methods=['POST'])
def edit_task(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            task_uid = request.form['rvw_uid_etask']
            task_nume = request.form['rvw_nume_etask']
            task_desc = request.form['rvw_desc_etask']
            task_term = request.form['rvw_term_etask']
            task_status = request.form['rvw_status']
            task_prog = request.form['rvw_prog_etask']
            task = rvw_structuri.Task.from_id(task_uid)
            task.nume = task_nume
            task.desc = task_desc
            task.termen = task_term + ", 00:00:00"
            task.progres = int(round(float(task_prog)))
            for i in range(0,4):
                if task_status == rvw_structuri.taskstatus[i]:
                    task.status = i
                    break
            task.participanti = []
            for memL in rvw_structuri.Membru.getAccepted():
                k = memL.nume+" - "+rvw_structuri.getRolByDisp(memL.rol)[2]
                if k in request.form and memL.uid not in task.participanti:
                    task.participanti.append(memL.uid)
            task.save()
            return "Schimbarile au fost salvate"
            
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'<tuid>/get_task', methods=['POST'])
def get_task(uid, tuid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            if request.content_type == 'application/json':
                task = rvw_structuri.Task.from_id(tuid)
                task_membri_list = []
                for puid in task.participanti:
                    memf = rvw_structuri.Membru.from_id(puid)
                    task_membri_list.append(memf.nume+" - "+rvw_structuri.getRolByDisp(memf.rol)[2])
                if rvw_structuri.getRolByDisp(mem.rol)[0] >= rvw_structuri.getRolByDisp(rvw_structuri.Membru.from_id(task.initiator).rol)[0]:
                    return jsonify(nume=task.nume, desc=task.desc, termen=task.termen, status=task.status,
                    progres=task.progres, participanti=task_membri_list)
                return "Nu ai permisiunea de a edita task-ul"
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'get_tasks', methods=['POST'])
def get_tasks(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            if request.content_type == 'application/json':
                return jsonify([rvw_structuri.Task.get_show(tf) for tf in rvw_structuri.Task.getFiles()])
    
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'submtask', methods=['POST'])
def submit_task(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            nume_task = request.form['rvw_nume_task']
            desc_task = request.form['rvw_desc_task']
            term_task = request.form['rvw_term_task']
            if nume_task and desc_task and term_task:
                term_task = term_task+", 00:00:00"
                try:
                    rvw_structuri.stringToDate(term_task)
                except:
                    return "Termenul limita nu este valid"
                task = rvw_structuri.Task(mem.uid, nume_task, desc_task, term_task, participanti=[])
                for memL in rvw_structuri.Membru.getAccepted():
                    k = memL.nume+" - "+rvw_structuri.getRolByDisp(memL.rol)[2]
                    if k in request.form and memL.uid not in task.participanti:
                        task.participanti.append(memL.uid)
                task.save()
                rvw_structuri.sendNotif("Task adaugat",mem.nume+" a adaugat un task")
                return "Task inregistrat"
            elif not nume_task:
                return "Numele taskului nu poate fi gol"
            elif not desc_task:
                return "Descrierea taskului nu poate fi goala"
            else:
                return "Termenul taskului nu poate fi gol"
        return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane simultan. Da refresh la pagina."
    return "Invalid"

@app.route(rvw_route_api_membri+'subinteres', methods=['POST'])
def submit_interese(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            mem.interese = []
            for interes in rvw_structuri.interese:
                if interes in request.form:
                    mem.interese.append(interes)
            mem.save()
            rvw_structuri.sendNotif("Interese",mem.nume+" si-a expus interesele")
            return "Interese salvate"
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'subprof', methods=['POST'])
def submit_profil(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            schimbat = False
            telefon = request.form['rvw_telefon']
            desc = request.form['rvw_desc']
            porecla = request.form['rvw_porecla']
            if not telefon == mem.telefon:
                if telefon.isdigit() and len(telefon) == 10 and telefon.startswith("07"):
                    schimbat = True
                    mem.telefon = telefon
                else:
                    return "Numarul de telefon nu este valid"
            if not desc == mem.descriere:
                schimbat = True
                mem.descriere = desc
            if not porecla == mem.porecla:
                if " " not in porecla or len(porecla.split(" ")) <= 2:
                    schimbat = True
                    mem.porecla = porecla
                else:
                    return "Nickname-ul nu este valid. Nu poate avea mai mult de doua cuvinte."
            if schimbat:
                mem.save()
                return "Informatiile au fost salvate"
            else:
                return "Nimic nu a fost schimbat"
            
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."

@app.route(rvw_route_api_membri+'get_t_gen', methods=['POST'])
def get_t_gen(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            return rvw_template.getGeneralTemplate(mem, uid)
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."
    

@app.route(rvw_route_api_membri+'get_t_gen_s', methods=['POST'])
def get_t_gen_s(uid):
    cookie = request.cookies.get("devs")
    if cookie:
        mem = rvw_structuri.Membru.getByLoguid(cookie)
        if mem and uid in mem.seccodes:
            return rvw_template.getScripts(mem, uid)
    return "Actiunea a fost blocata din motive de securitate. Cel mai probabil contul este folosit de mai multe persoane. Da refresh la pagina."
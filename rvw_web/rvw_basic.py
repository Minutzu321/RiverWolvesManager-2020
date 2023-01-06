from rvw_creier.rvw_info import Informatie
from rvw_creier.rvw_facerecog import prezi
from rvw_web import app, request, jsonify, send_from_directory, make_response, base64, logging, redirect
from rvw_structuri import *
from rvw_template import *
import rvw_creier
import rvw_fisiere
import requests
import qrcode
from io import BytesIO
from PIL import Image
import base64
import uuid
import logging

def postRequest(url, req):
  return requests.post(url = url, data = req).text

def getErrModal(text):
  return '<div class="modal fade modal-mini modal-primary show" id="errmodal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" style="display: block;" aria-modal="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-body"><p>'+text+'</p></div><div class="modal-footer justify-content-center"><button type="button" class="btn btn-link btn-neutral" data-dismiss="modal" onclick=\'document.getElementById("errmodal").style.display = "none";\'>Inchide</button></div></div></div></div>'

@app.route('/google423c88ae56498dd0.html', methods=['GET'])
def boti():
    return render_template("gverif.html")

@app.route('/buget')
def get_pdf():
    # return rvw_fisiere.getWebFilesPath("buget.xlsx")
    # with open(rvw_fisiere.getWebFilesPath("buget.xlsx"), mode='rb') as bfile:
        # response = make_response(bfile.read())
        # response.headers['Content-Type'] = 'application/pdf'
        # response.headers['Content-Disposition'] = \
        #     'inline; filename=Buget RiverWolves.pdf'
        # return response
    return send_from_directory(rvw_fisiere.getWebFilesPath(""),"Buget RiverWolves.xlsx")
    # import codecs
    # with open(rvw_fisiere.getWebFilesPath("buget.xlsx"), mode='rb') as bfile:
    #     resp = Response(codecs.encode(bfile,"base64"))
    #     resp.headers['Content-Disposition'] = "inline; filename=Buget"
    #     resp.mimetype = 'application/pdf'
    #     return resp

#routes
@app.route('/', methods=['GET'])
def home_basic():
    cookie = request.cookies.get("devs")
    if not cookie: return render_template("home_basic.html")

    user = Membru.getByLoguid(cookie)
    if user:
        if user.status == "acceptat" and not "inactiv" in user.infos:
            return render_template("home_basic.html", red=True)
        else: 
            return render_template("home_basic.html", apli=True)

    return render_template("home_basic.html")

@app.route('/panopticon/<idq>', methods=['GET', 'POST'])
def panopticon(idq):
    if request.method == 'POST':
        deli = int(request.form['del'])
        if deli == 1:
            return "deleted"
        else:
            nume = request.form['nume']
            info = request.form['info']
            iob = rvw_creier.Informatie.getByNume(nume)
            pat = rvw_creier.getFaceFiles()[int(idq)]
            if iob:
                if pat not in iob.pat:
                    iob.pat.append(pat)
                if len(info) > 0:
                    iob.infos = info
                iob.save()
                rvw_creier.antreneaza()
                return "saved1 "+nume+" "+info
            else:
                if len(nume) < 3:
                    nume = None
                rvw_creier.Informatie([pat], nume=nume, infos=info).save()
                rvw_creier.antreneaza()
                return "saved2 "+nume+" "+info

    dpth = rvw_creier.getFaceFiles()[int(idq)]
    im = Image.open(rvw_fisiere.getCreierPath("facerecog",dpth)+"imagine.png")
    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    image_data = base64.b64encode(buffered.getvalue())
    if not isinstance(image_data, str):
        image_data = image_data.decode()
    data_url = 'data:image/jpg;base64,' + image_data

    encs = rvw_creier.getFaceData(dpth)
    prezis = rvw_creier.prezi(encs["encodings"])
    ziob = rvw_creier.Informatie.getByPat(dpth)
    dats = []
    for mem_id in Membru.getFiles():
        dats.append('"'+Membru.from_id(mem_id).nume+'"')
    for mem_id in Informatie.getFiles():
        dats.append('"'+Informatie.from_id(mem_id).nume+'"')
    proc = 0
    znume = ""
    zinfo = ""
    if prezis:
        znume = prezis[0].nume
        zinfo = prezis[0].infos
        proc = int(((1-prezis[1])*100))
    if ziob:
        znume = ziob.nume
        zinfo = ziob.infos
    return render_template("panopticon.html", scrpt=', '.join(dats), proc=proc, pag=int(idq), lat=encs["lat"], lng=encs["lng"], info=encs["timestamp"], src=data_url, prev=(int(idq)-1) , next=(int(idq)+1), numerm=znume, inform=zinfo)

def getMembriNumere():
    voluntari = 0
    alumni = 0
    mecanici = 0
    programatori = 0
    media = 0
    designeri = 0
    mentori = 0
    for mem in Membru.getAccepted():
        if getRolByDisp(mem.rol)[3] == 885 and len(mem.interese) > 0:
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
    return [voluntari,designeri,mecanici,programatori,media,alumni,mentori, designeri+voluntari+mecanici+media+programatori]

@app.route('/membru', methods=['GET'])
def home_membru():
    cookie = request.cookies.get("devs")
    if not cookie: return render_template("home_basic.html")

    user = Membru.getByLoguid(cookie) 
    if user and len(cookie)>6:
        if user.status == "acceptat" and not "inactiv" in user.infos:
            qr = qrcode.QRCode(
                border=1,
            )
            qr.add_data(user.qr)
            qr.make(fit=True)
            output = BytesIO()
            im = qr.make_image(fill_color="black", back_color="white")
            im.save(output, format='JPEG')
            im_data = output.getvalue()
            image_data = base64.b64encode(im_data)
            if not isinstance(image_data, str):
                image_data = image_data.decode()

            porecla = user.porecla
            if not porecla: porecla=""
            dispname = user.nume
            if user.porecla: dispname = user.porecla

            uid = str(uuid.uuid4())
            seccs = user.seccodes
            seccs.append(uid)
            while len(seccs) > 2:
                seccs.pop(0)
            user.seccodes = seccs
            user.save()

            lvl = getRolByDisp(user.rol)[0]

            task_membri_list = []

            interese = []

            if not user.interese:
                interese = rvw_structuri.interese

            memnumbs = getMembriNumere()
            mems = '''
            <div class="card">
            <canvas id="statsMembri"></canvas>
            <div class="card-footer text-muted mb-2"><b>Total: </b>'''+str(memnumbs[7])+'''</div>
            </div>

            <script>var config = {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [
                            '''+str(memnumbs[0])+''',
                            '''+str(memnumbs[1])+''',
                            '''+str(memnumbs[2])+''',
                            '''+str(memnumbs[3])+''',
                            '''+str(memnumbs[4])+''',
                            '''+str(memnumbs[5])+''',
                            '''+str(memnumbs[6])+'''
                        ],
                        backgroundColor: [
                            'rgb(255, 253, 119)',
                            'rgb(187, 189, 246)',
                            'rgb(56, 134, 151)',
                            'rgb(39, 16, 51)',
                            'rgb(250, 131, 52)',
                            'rgb(255, 232, 130)',
                            'rgb(213, 41, 65)'
                        ],
                        label: 'Statistici'
                    }],
                    labels: [
                        'Voluntari',
                        'Designeri',
                        'Mecanici',
                        'Programatori',
                        'Media',
                        'Alumni',
                        'Mentori'
                    ]
                },
                options: {
                    responsive: true,
                }
            };
            window.onload = function() {
                var ctx = document.getElementById('statsMembri').getContext('2d');
                window.myPie = new Chart(ctx, config);
            };</script>
            '''

            # mems.format(, str(memnumbs[1]), str(memnumbs[2]), str(memnumbs[3]), str(memnumbs[4]), str(memnumbs[5]), str(memnumbs[6]))
            membrilistsorted = Membru.getAccepted()
            membrilistsorted.sort(key=lambda x: x.getImportanta(), reverse=True)
            for cnv in membrilistsorted:
                task_membri_list.append(cnv.nume+" - "+getRolByDisp(cnv.rol)[2])
                if getRolByDisp(cnv.rol)[2] != 'Mentor':
                    interesw = ""
                    for i in range(len(cnv.interese)):
                        interesw += cnv.interese[i]
                        if i != len(cnv.interese)-1:
                            interesw += ", "
                    if not interesw: interesw="?"
                    objs = [
                            "<h3><b>"+cnv.nume+"</b></h3>",
                            "<h5><b>Email: </b>"+cnv.email+"</h5>",
                            "<h5><b>Data nasterii: </b>"+cnv.data_nastere.replace(", 00:00:00","")+"</h5>",
                            "<h5><b>Rol: </b>"+getRolByDisp(cnv.rol)[2]+"</h5>",
                            ]
                    if lvl > 2 or getRolByDisp(cnv.rol)[0] > 4:
                        objs.append("<h5><b>Telefon: </b>"+str(cnv.telefon)+"</h5>")
                    if lvl > 3:
                        objs.append("<h5><b>Incredere: </b>"+str(cnv.incredere)+"</h5>")
                    
                    objs.append("<h5><b>Interese: </b>"+interesw+"</h5>")

                    mems += Div("card card-body col-md-10 ml-auto col-xl-5 mr-auto", objs).toHTML()

            return render_template("home_user.html", displayname=dispname, username=user.nume, qrcode=image_data,
             email=user.email, telefon=user.telefon, rol=user.rol, porecla=porecla, desc=user.descriere, seccode=uid,
             lvl=lvl, nume_membri_list=task_membri_list, uid=user.uid, interese=interese, mems=mems, generaldivs=getGeneralTemplate(user,uid))
        else:
            return render_template("home_basic.html",apli=True)
    else:
        resp = make_response(render_template("home_basic.html"))
        if not cookie:
            return resp
        if not len(cookie) <= 6:
            resp.set_cookie("devs","pa",max_age=0)
        return resp



@app.route('/register', methods=['GET', 'POST'])
def register_basic():
    cookie = request.cookies.get("devs")
    if cookie is None or Membru.from_id(cookie):
        l = [roluri[i][1] for i in range(5)]
        if request.method == 'POST':
            if request.form['g-recaptcha-response']:
                req = {
                    'secret': '6LcZQekUAAAAALVxmZ9xizl2thEkiALdObxkgCgZ',
                    'response': request.form['g-recaptcha-response']
                }
                captcha = postRequest("https://www.google.com/recaptcha/api/siteverify",req)
                if json.loads(captcha)["success"]:
                    datalist = request.form['data_de_inregistrare'].split("@gogoq")
                    logging.info(datalist)
                    ip=""
                    for data in datalist:
                        if "ip=" in data:
                            ip = data.replace("ip=","")
                        if "loc=" in data and "loc=RO" not in data:
                            return render_template("register.html", roluri=l,
                             err=getErrModal("Only users from Romania can apply. If you think this is a mistake, contact us on instagram<br>@riverwolves.049"))
                    if not ip:
                        return render_template("register.html", roluri=l,
                         err=getErrModal("A aparut o problema. Contacteaza-ne pe instagram daca vrei sa aplici<br>@riverwolves.049"))
                    if isBanned(ip):
                        return render_template("register.html", roluri=l,
                         err=getErrModal("IP-ul tau este in blacklist, daca consideri ca s-a produs o greseala, contacteaza-ne pe instagram<br>@riverwolves.049"))
                    nume = request.form['nume']
                    email = request.form['email']
                    telefon = request.form['telefon']
                    data_nastere = request.form['data_nastere']
                    rol = request.form['rol']
                    nume_array = nume.replace("-"," ").split(" ")

                    if len(nume_array) < 2 or len(nume_array) >= 4:
                        return render_template("register.html", roluri=l,
                         err=getErrModal("Numele nu este valid"), email=email, telefon=telefon,
                          datan=data_nastere, srol=rol)

                    if len(telefon) != 10:
                        return render_template("register.html", roluri=l,
                         err=getErrModal("Numarul de telefon nu este valid"), nume=nume, email=email,
                          datan=data_nastere, srol=rol)

                    if rol not in l:
                        return render_template("register.html", roluri=l,
                         err=getErrModal("Rolul la care ai aplicat nu este valabil"),
                          nume=nume, email=email, telefon=telefon, datan=data_nastere)

                    if nume.replace(" ","").replace("-","").isalpha() and "@" in email and telefon.isdigit() and rol:
                        if Membru.getByNume(nume) is not None:
                            return render_template("register.html", roluri=l,
                             err=getErrModal("Numele este deja folosit"))

                        if Membru.getByEmail(email) is not None:
                            return render_template("register.html", roluri=l,
                             err=getErrModal("Email-ul este deja folosit"))

                        if Membru.getByTelefon(telefon) is not None:
                            return render_template("register.html", roluri=l,
                             err=getErrModal("Numarul de telefon este deja folosit"))

                        data_nastere = data_nastere+", 00:00:00"
                        try:
                            dnastere = stringToDate(data_nastere)
                            if calculate_age(dnastere) < 13:
                                return render_template("register.html", roluri=l,
                                 err=getErrModal("Un membru sau voluntar nu poate avea varsta mai mica de 13 ani."),
                                  nume=nume, email=email, telefon=telefon, srol=rol)

                            if calculate_age(dnastere) > 90:
                                return render_template("register.html", roluri=l,
                                 err=getErrModal("Un membru sau voluntar nu poate avea varsta mai mare de 90 de ani."),
                                  nume=nume, email=email, telefon=telefon, srol=rol)
                        except:
                            return render_template("register.html", roluri=l,
                             err=getErrModal("Data nasterii nu este valida<br>Scriere corecta: zi/luna/an"),
                             nume=nume, email=email, telefon=telefon, srol=rol)

                        resp = make_response(render_template("register.html", roluri=l,
                         err=getErrModal("Solicitarile de roluri sunt momentan blocate.")))

                        membru = Membru(nume=nume,email=email,telefon=telefon,data_nastere=data_nastere,rol=rol,ips=[ip])
                        membru.save()
                        resp.set_cookie("devs",membru.loguid, max_age = 60 * 60 * 24 * 365 * 2, secure=True, httponly=True, samesite='Lax')
                        sendNotif(nume+" a aplicat","Decide-i soarta")
                        return resp
                    else:
                        return render_template("register.html", roluri=l, err=getErrModal("A aparut o eroare. Reintrodu informatiile"))
            else:
                return render_template("register.html", roluri=l, err=getErrModal("Bifeaza casuta de la captcha"))
        return render_template("register.html", roluri=l)
    else:
        return redirect("https://ro049.com/membru", code=302)





@app.route('/login', methods=['GET', 'POST'])
def login_basic():
    if request.method == 'POST':
        uid = request.form['rvw_id']
        datalist = request.form['data_de_inregistrare'].split("@gogoq")
        ip=""
        for data in datalist:
            if "ip=" in data:
                ip = data.replace("ip=","")
        if isBanned(ip):
            return render_template("login.html",err=getErrModal("Adresa ta se afla in blacklist, daca consideri ca s-a produs o greseala, contacteaza-ne pe instagram<br>@riverwolves.049"))
        
        if '@' in uid:
            uid = uid.replace("  ","")
            uid = uid.replace("  ","")
            uid = uid.replace(" ","")
            uid = uid.replace(" ","")
            mem = Membru.getByEmail(uid)
            if mem:
                rvw_structuri.sendEmail(mem.email,"Cont RiverWolves","Cerere acces cont","Apasa butonul de mai jos pentru a-ti accesa contul.","","LOGHEAZA-TE","https://ro049.com/login?log="+mem.loguid)
                return render_template("login.html",err=getErrModal("Ti-a fost trimis un email cu link-ul contului."))
            else:
                return render_template("login.html",err=getErrModal("Contul nu a fost gasit. Verifica email-ul si incearca din nou."))
        mem = Membru.getByLoguid(uid)
        if mem: 
            if "inactiv" in mem.infos:
                return render_template("login.html",err=getErrModal("Contul tau a fost dezactivat de la inactivitate. Aceasta actiune este ireversibila."))
            if mem.status == "acceptat":
                if ip not in mem.ips:
                    # if mem.ips:
                    #     sendEmail(mem.email,"Cont Accesat","Alerta","Contul a fost accesat de pe o adresa necunoscuta","Daca tu ai")
                    mem.ips.append(ip)
                    mem.save()
                res = make_response(redirect('https://ro049.com/membru', code=302))
                res.set_cookie("devs",mem.loguid,max_age=90 * 60 * 60 * 24)
                rvw_structuri.sendNotif("Logare",mem.nume)
                return res
            else:
                if mem.status == "pending":
                    sendNotif("Imposibilul s-a intamplat!",mem.nume)
                return render_template("login.html",err=getErrModal("Contul nu este activ."))
        else:
            return render_template("login.html",err=getErrModal("Codul nu este valid"))

    cookie = request.cookies.get("devs")
    if cookie:
        user = Membru.getByLoguid(cookie)
        if user and user.status == 'acceptat':
            return redirect('https://ro049.com/membru', code=302)
    
    if 'log' in request.args:
        log = request.args['log']
        if log and len(log)==36:
            return render_template("login.html",log=log)
    return render_template("login.html")

from flask import jsonify
from flask import request


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
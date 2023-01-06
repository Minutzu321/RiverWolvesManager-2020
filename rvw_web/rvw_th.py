from rvw_web.rvw_sockets import rbtfd
from rvw_structuri.rvw_contact import sendEmail
from rvw_web import app, jsonify, request, render_template, make_response, redirect
import rvw_treasurehunt
from unidecode import unidecode
from rvw_structuri import sendNotif, Rezervare, Membru, Player, getRolByDisp
import requests
import json
import logging

rvw_route_th = "/th"

def postRequest(url, req):
  return requests.post(url = url, data = req).text

@app.route(rvw_route_th+"/conditii", methods=['POST'])
def conditii_th():
    cookie = request.cookies.get("player")
    if cookie:
        player = Player.from_id(cookie)
        if player and not player.semnatura:
            semnatura = request.form['rvw_semnatura']
            player.semnatura = semnatura
            player.save()
            return "Semnatura a fost salvata"
        return "Codul nu este valid!"
    return "Nu esti logat."

@app.route(rvw_route_th+"/log", methods=['POST'])
def log_th():
    cod = request.form['rvw_cod']
    player = Player.getByCod(cod)
    if player:
        res = make_response(redirect('https://ro049.com/th'))
        res.set_cookie("player",player.uid,max_age=200 * 60 * 60 * 24)
        return res
    return "Codul nu este valid!"



@app.route(rvw_route_th, methods=['GET'])
def home_th():
    cookie = request.cookies.get("player")
    if cookie:
        player = Player.from_id(cookie)
        if player:
            return render_template("th/jucatori.html", cod=player.cod)
        
    return render_template("th/scan.html")

@app.route(rvw_route_th+"/rezervare", methods=['GET'])
def arez_th():
    cookie = request.cookies.get("devs")
    membru = Membru.getByLoguid(cookie)
    if cookie and membru:
        
        divs = ""
        for rez_id in Rezervare.getFiles():
            rez = Rezervare.from_id(rez_id)
            divs += '''
            <div>
                <h3>Nume: '''+rez.nume+'''</h3>
                <h3>Telefon: '''+rez.telefon+'''</h3>
                <h3>Persoane: '''+rez.persoane+'''</h3>
            </div>
            <hr/>
            '''
        return render_template("th/rez.html", divs=divs)

    return "Nu."

@app.route(rvw_route_th+"/admin", methods=['GET'])
def admin_th():
    cookie = request.cookies.get("devs")
    membru = Membru.getByLoguid(cookie)
    if cookie and membru:
        if getRolByDisp(membru.rol)[0] <= 1:
                return "Nup."
        lss = ""
        
        for ind in rvw_treasurehunt.getIndicii():
            indiciu = rvw_treasurehunt.getIndiciu(ind, False)
            intrb = indiciu["intrebare"]
            lss += "L.marker(["+str(indiciu["lat"])+", "+str(indiciu["lng"])+']).addTo(mymap).bindPopup(\''+intrb+'\');'
            if not 'poza' in intrb:
                lss += '''
                    L.circle(['''+str(indiciu["lat"])+''', '''+str(indiciu["lng"])+'''], {
                        color: 'red',
                        fillColor: '#f03',
                        fillOpacity: 0.1,
                        radius: '''+str(indiciu["acuratete"])+'''
                    }).addTo(mymap);
                '''
        return render_template("th/hartam.html", ls=lss)

    return "Nu."

@app.route(rvw_route_th+"/rezerva", methods=['POST'])
def rezerva_th():
    if request.form['g-recaptcha-response']:
                req = {
                    'secret': '-------------',
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
                            return "Only users from Romania can apply. If you think this is a mistake, contact us on instagram - @riverwolves.049"
                    if not ip:
                        return "A aparut o problema. Contacteaza-ne pe instagram daca vrei sa rezervi un bilet - @riverwolves.049"
                    nume = request.form['rvw_nume']
                    telefon = request.form['rvw_tel']
                    pers = request.form['rvw_pers']
                    if not nume or len(nume) < 5 or len(nume.split(" ")) < 2:
                        return "Intordu numele intreg"
                    if not telefon.isdigit() or len(telefon) != 10 or not telefon.startswith("07"):
                        return "Numarul de telefon nu este valid."
                    if Rezervare.getByTelefon(telefon):
                        return "Numarul de telefon este deja inregistrat."
                    if len(Rezervare.getByIP(ip)) == 0:
                        sendNotif("Rezervare",nume)
                        Rezervare(nume=nume, telefon=telefon, persoane=pers, ips=[ip]).save()
                        return "Rezervare inregistrata. Va asteptam!"
                    else:
                        return "Deja ai facut o rezervare."
    return "Rezolva captcha-ul pentru a rezerva."

@app.route(rvw_route_th+"/casier", methods=['GET','POST'])
def casier_th():
    cookie = request.cookies.get("devs")
    membru = Membru.getByLoguid(cookie)
    if cookie and membru:
        if getRolByDisp(membru.rol)[0] <= 1:
                return "Ai rol de voluntar si nu ai permisiunea de a adauga jucatori."
        if request.method == 'POST':
            nume = request.form['nume']
            tel = request.form['tel']
            pickup = request.form['pickup']
            dif = int(request.form['dificultate'])
            pers = int(request.form['pers'])
            plata = float(request.form['plata'])

            relax = False
            copii = False
            adolescenti = False
            adulti = False
            try:
                relax = request.form['relax']
                relax = True
            except:
                pass
            try:
                copii = request.form['copii']
                copii = True
            except:
                pass
            try:
                adolescenti = request.form['adolescenti']
                adolescenti = True
            except:
                pass
            try:
                adulti = request.form['adulti']
                adulti = True
            except:
                pass

            ply = Player(nume=nume, telefon=tel, platit=plata, persoane=pers, dif=dif, pickup=pickup, relax=relax, copii=copii, adolescenti=adolescenti, adulti=adulti)
            ply.save()

            return ply.cod
        return render_template("th/casier.html")
    return "No cookie!"

@app.route(rvw_route_th+"/indicii", methods=['GET','POST'])
def indicii_th():
    cookie = request.cookies.get("devs")
    # return cookie
    membru = Membru.getByLoguid(cookie)
    if cookie and membru:
        if request.method == 'POST':
            ind = request.form['rvw_ind']
            poz = request.form['rvw_poza']
            rasp = request.form['rvw_rasp']
            locatie_coord = request.form['locatie_coord'].split(",")
            lat = float(locatie_coord[0])
            lng = float(locatie_coord[1])
            acc = float(locatie_coord[2])
            ilocat = False
            ipoza = False
            try:
                ilocat = request.form['locatie']
                ilocat = True
            except:
                pass
            try:
                ipoza = request.form['poza']
                ipoza = True
            except:
                pass
            dif = int(request.form['rvw_dif'])
            if ilocat:
                ind += "locatie"
            if ipoza:
                ind += "poza"

            membru.infos.append([
                "indiciu",
                rvw_treasurehunt.addIndiciu(lat, lng, poz, acc, dif, ind, rasp)
            ])
            membru.save()

            return "a mers"
        return render_template("th/indp.html")
    return "No cookie!"


@app.route("/thunt_demo", methods=['GET','POST'])
def zaha_th():
    best = None
    best_id = None
    for indiciu_id in rvw_treasurehunt.getIndicii():
        indiciu = rvw_treasurehunt.getIndiciu(indiciu_id, False)
        if not best:
            if not request.cookies.get(indiciu_id):
                best = indiciu
                best_id = indiciu_id
        elif indiciu['timp'] < best['timp'] and not request.cookies.get(indiciu_id):
            best = indiciu
            best_id = indiciu_id
    if request.method == 'POST':
        if request.form['zaha_rasp'].lower() == best['raspuns'].lower():
            res = make_response(redirect('/thunt_demo'))
            res.set_cookie(best_id,"1",max_age=200 * 60 * 60 * 24)
            return res

    if best:
        finind = '''<h2>'''+best['intrebare']+'''</h2>'''
        if 'locatie' in best['intrebare']:
            finind = finind.replace("locatie", "")
            finind += '''<!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
                integrity=""
                crossorigin=""/>
                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
                integrity=""
                crossorigin=""></script>
            </head>
            <body>
            <div id="mapid" style="height: 500px"></div>
                <script>
                    var mymap = L.map('mapid').setView([51.505, -0.09], 13);
                    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                        attribution: 'Facut pentru Zaha',
                        maxZoom: 20,
                        id: 'mapbox/streets-v11',
                        tileSize: 512,
                        zoomOffset: -1,
                        accessToken: ''
                    }).addTo(mymap);
                    var marker_loc = L.marker([51.5, -0.09]).addTo(mymap);
                    marker_loc.bindPopup("Esti aici.").openPopup();
                    var circle = L.circle(['''+str(best['lat'])+''', '''+str(best['lng'])+'''], {
                        color: 'red',
                        fillColor: '#f03',
                        fillOpacity: 0.1,
                        radius: '''+str(best['acuratete'])+'''
                    }).addTo(mymap);
                    getLocation();
                    var intervalId = setInterval(function() {
                        getLocation();
                    }, 2000);
                    function getLocation() {
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(showPosition);
                        } else {
                            x.innerHTML = "Geolocation is not supported by this browser.";
                        }
                    }

                    var frst = true;
                    function showPosition(position) {
                        marker_loc.setLatLng([position.coords.latitude,position.coords.longitude]);
                        if(frst){
                            mymap.setView([position.coords.latitude,position.coords.longitude], 16)
                        }
                        frst = false;
                    }
                </script>
            </body>
            </html>
            <br>
            '''
        if 'poza' in best['intrebare']:
            finind = finind.replace("poza", "")
            finind += '''<img id="img" src="'''+best['poza']+'''" /><br>'''
        finind += '''
                <br>
                <form class="form" method="post" action="thunt_demo">
                    <input name="zaha_rasp" type="text" class="form-control" placeholder="Raspuns" required autocomplete="off">
                </form>
            '''
    else:
        finind = '''<iframe src="https://giphy.com/embed/W8krmZSDxPIfm" width="100%" height="100%" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>'''

    return render_template("pln.html",
    indiciu=finind)
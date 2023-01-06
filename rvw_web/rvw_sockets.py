from rvw_web import app, request, logging
from flask import request, render_template
from rvw_structuri import Player, Locatie, sendNotif
from rvw_treasurehunt import getIndiciu, getIndicii
import geopy.distance

import unidecode
from difflib import SequenceMatcher

robotfeedclients = []
clienti = []



class Client:
    def __init__(self, ws, uid):
        self.ws = ws
        self.uid = uid

@app.route('/robotfeed')
def rbtfd():
    return render_template('robot_feed.html')

# @app.route('/rvw-api/sockconn')
# def sockconn():
#     global robotfeedclients
#     if request.environ.get('wsgi.websocket'):
#         ws = request.environ['wsgi.websocket']
#         while True:
#             message = ws.receive()
#             if message == 'sockconn':
#                 robotfeedclients.append(ws)


def get_th():
    cookie = request.cookies.get("player")
    if cookie:
        player = Player.from_id(cookie)
        if player:
            if not player.semnatura:
                return render_template("th/semnatura.html")
            if not player.indiciu_curent:
                return render_template("th/countdown.html")    

            
            
            return "Timpul a expirat. Cine a facut cele mai multe indicii a castigat."
    # return apropiata

def transformastr(strng):
    strng = strng.lower()
    strng.replace(" ","")
    strng.replace(".","")
    strng.replace(",","")
    strng.replace("-","")
    strng = unidecode.unidecode(strng)
    return strng
import random
intamp = ["Gaseste voluntarii de la Cimitirul Eroilor",
            "Gaseste voluntarii de la Monument",
            "Gaseste voluntarii din parcul Victoria",
            "Gaseste voluntarii din parcul Personalitatilor",
            "Gaseste voluntarii din parcul Tavs(in spate la Select)",
            "Gaseste voluntarii de pe Ciuperca (In fata la Mars)"]

@app.route('/rvw-api/thsckt/<uid>')
def thkt(uid):
    global clienti
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        client = None
        for cli in clienti:
            if cli.uid == uid:
                cli.ws = ws
                client = cli
                break

        if not client:
            client = Client(ws, uid)
            clienti.append(client)

        while not ws.closed:
            try:
                message = ws.receive()
                
                if message == 'get':
                    ws.send(get_th())
                    continue
                if message.startswith("%coord%"):
                    message = message.replace("%coord%","").split(",")
                    player = Player.getByCod(client.uid)
                    player.locatie = Locatie(lat=float(message[0]), long=float(message[1]), acc=float(message[2])).to_json()
                    player.save()
                if message.startswith("%rasp%"):
                    # message = transformastr(message.replace("%rasp%",""))
                    # player = Player.getByCod(client.uid)
                    # raspuns = transformastr(getIndiciu(player.indiciu_curent,False)['raspuns'])
                    ws.send("!1!"+"Timpul a expirat.")
                # for client in ws.handler.server.clients.values():
                #     if client.ws in robotfeedclients and client.ws is not ws:
                #         client.ws.send(message)
            except Exception as excep:
                app.logger.info("EXCEP: "+str(excep))
                

    return ""

@app.route('/rvw-api/robotfeed')
def robotfeed():
    global robotfeedclients
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while not ws.closed:
            try:
                message = ws.receive()
                app.logger.info("MESAJ: "+message)
                if message == 'robotfeed':
                    robotfeedclients.append(ws)
                    continue
                for client in ws.handler.server.clients.values():
                    if client.ws in robotfeedclients and client.ws is not ws:
                        client.ws.send(message)
            except Exception as excep:
                app.logger.info("EXCEP: "+str(excep))
                    
            # torem = []
            # for tclient in robotfeedclients:
            #     if tclient not in ws.handler.server.clients.values():
            #         torem.append(tclient)
            # for rem in torem:
            #     robotfeedclients.remove(rem)

    return ""

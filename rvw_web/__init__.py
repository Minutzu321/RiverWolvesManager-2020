from flask import Flask, request, jsonify, url_for, make_response, render_template, redirect, flash, send_from_directory, Response
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json
import logging
import os
from multiprocessing import Process
from io import BytesIO
import base64
from PIL import Image
from sys import platform

import rvw_fisiere

app = Flask('RiverWolves')

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response

from .rvw_api_android import *
from .rvw_api_indicii import *
from .rvw_api_membri import *
from .rvw_api_playeri import *
from .rvw_api_minecraft import *

from .rvw_basic import *
from .rvw_th import *
from .rvw_test import *
from .rvw_sockets import *
from .rvw_timer import *
from .rvw_teo import *

def runServer():
    app.secret_key = '--------------------------------'
    # app.config['SESSION_TYPE'] = 'filesystem'
    logging.basicConfig(filename='loguri.log',level=logging.INFO)
    # app.use_debugger = True
    # app.use_reloader = True
    # if not(platform == "linux" or platform == "linux2") :
    # app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

def start_web():
    runServer()


# #SITE
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/antreneaza', methods=['GET', 'POST'])
# def antreneaza():
#     proceseaza_uploadate()
#     dir_rec = os.listdir(rvw_fisiere.getPozeDeRecunoscutPath())
#     if len(dir_rec) > 0:
#         im = Image.open(rvw_fisiere.getPozeDeRecunoscutPath()+dir_rec[0])
#         if request.method == 'POST':
#             pers = request.form['pers']
#             info = request.form['info']
#             if not info:
#                 info = []
#             else:
#                 info = info.split(',')
#             adauga_imagine(im,pers,info)
#             os.remove(rvw_fisiere.getPozeDeRecunoscutPath()+dir_rec[0])
#             return redirect("/antreneaza")
#         output = BytesIO()
#         im.save(output, format='JPEG')
#         rec = recunoastere_faciala(output)[0][0]
#         im_data = output.getvalue()
#         image_data = base64.b64encode(im_data)
#         if not isinstance(image_data, str):
#             image_data = image_data.decode()
#         data_url = 'data:image/jpg;base64,' + image_data
#         return '''
#         <!doctype html>
#         <title>Antreneaza</title>
#         <img src="'''+data_url+'''">
#         <h1>Cine este persoana din imagine?</h1>
#         <form method=post enctype=multipart/form-data>
#         <input type=text name=pers value='''+rec+'''>
#         <p>Informatii despre persoana:</p>
#         <input type=text name=info>
#         <input type=submit value=Trimite>
#         </form>
#         '''
#     return 'nu avem ce sa antrenam :('

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     cookie = request.cookies.get("SID")
#     if cookie is None:
#         return render_template("home_basic.html")
#     else:
#         if userExistsUUID(cookie):
#             user = User(cookie)
            
#             if user.status == "acceptat":
#                 return render_template("home_user.html")
#             return render_template("home_basic.html")
#         else:
#             resp = make_response(render_template("home_basic.html"))
#             resp.set_cookie('SID', '', expires=0)
#             return resp
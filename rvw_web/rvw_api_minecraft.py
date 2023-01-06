import os, sys
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from rvw_web import app
from flask import send_file

rvw_route_api_minekreft = "/rvw-api/minekreft/"

#genereaza o imagine customizata pentru serverul de minecraft
@app.route(rvw_route_api_minekreft+'get_skin/<nume>')
def get_skin(nume):
    response = requests.get("https://minotar.net/body/"+nume+"/100.png")
    skin = Image.open(BytesIO(response.content))
    printable = Image.open("static/img/bg_Skin.png")
    Sw, Sh = skin.size
    Pw, Ph = printable.size
    printable.paste(skin, (int(Pw/2)-int(Sw/2),int(Ph/2)-int(Sh/2)), skin)
    img_io = BytesIO()
    printable.save(img_io, 'PNG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
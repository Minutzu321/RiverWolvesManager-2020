from rvw_web import app, jsonify, request
import rvw_treasurehunt
import rvw_structuri
from PIL import Image
from io import BytesIO
import base64

rvw_route_api_indicii = "/rvw-api/indicii/"

#INDICII
@app.route(rvw_route_api_indicii+'get_indicii', methods=['POST'])
def get_indicii():
    return jsonify(rasp=rvw_treasurehunt.getIndicii())


@app.route(rvw_route_api_indicii+'get_indiciu_android', methods=['POST'])
def get_indiciu_android():
    if request.get_json():
        try:
            req = request.get_json()
            indiciu = req['indiciu']
            return jsonify(rasp=rvw_treasurehunt.getIndiciu(indiciu,True))
        except:
            return jsonify(rasp="eroare")
    return jsonify(rasp="eroare")
    

@app.route(rvw_route_api_indicii+'adauga_indiciu', methods=['POST'])
def adauga_indicii():
    if request.get_json():
        try:
            req = request.get_json()
            lat = req['lat']
            lng = req['lng']
            poza = req['poza']
            acuratete = req['acuratete']
            dif = req['dif']
            indiciu = req['indiciu']
            rasp = req['rasp']
            rvw_treasurehunt.addIndiciu(lat,lng,poza,acuratete,dif,indiciu,rasp)
            return "succes"
        except:
            return "eroare1"
    return "eroare2"

@app.route(rvw_route_api_indicii+'adauga_bmp', methods = ['POST'])
def handle_request_bmp():
    imagefile = request.files['image']
    filename = imagefile.filename
    im = Image.open(imagefile)
      
    output = BytesIO()
    im.save(output, format='JPEG')
    im_data = output.getvalue()
    image_data = base64.b64encode(im_data)
    if not isinstance(image_data, str):
        image_data = image_data.decode()
    data_url = 'data:image/jpg;base64,' + image_data
    rvw_treasurehunt.setPozaByPozaUUID(filename, data_url)
    return "Imagine succes"
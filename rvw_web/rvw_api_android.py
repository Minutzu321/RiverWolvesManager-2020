from rvw_web import app, request, jsonify
import rvw_structuri

rvw_route_api_android = "/rvw-api/androidapi/"

apass = "-----------"

@app.route(rvw_route_api_android+'ban_membru', methods=['POST'])
def ban_membru():
    req = request.get_json()
    if req['pas'] == apass:
        uid = req['uid']
        membru = rvw_structuri.Membru.from_id(uid)
        membru.status = "banat"
        membru.save()
        return jsonify(rasp=True)
    return jsonify(rasp=False)

@app.route(rvw_route_api_android+'acc_membru', methods=['POST'])
def acc_membru():
    req = request.get_json()
    if req['pas'] == apass:
        uid = req['uid']
        membru = rvw_structuri.Membru.from_id(uid)
        membru.status = "acceptat"
        membru.save()
        rvw_structuri.sendEmail(membru.email,"Cont RiverWolves","Cont procesat","Bine ai venit in echipa RiverWolves!","Contul tau a fost creat! Apasa butonul de mai jos pentru a-l accesa.","LOGHEAZA-TE","https://ro049.com/login?log="+membru.loguid)
        return jsonify(rasp=True)
    return jsonify(rasp=False)

@app.route(rvw_route_api_android+'get_membru', methods=['POST'])
def get_membru():
    req = request.get_json()
    if req['pas'] == apass:
        uid = req['uid']
        retstruc = rvw_structuri.Membru.from_id(uid)
        rezq = jsonify(rasp=retstruc.to_json())
        return rezq
    return jsonify(rasp="eroare")

@app.route(rvw_route_api_android+'get_membri', methods=['POST'])
def get_membri():
    req = request.get_json()
    if req['pas'] == apass:
        return jsonify(rasp=rvw_structuri.Membru.getFiles())
    return jsonify(rasp="eroare")
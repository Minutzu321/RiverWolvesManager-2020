from rvw_web import app, jsonify
import rvw_structuri

rvw_route_api_playeri = "/rvw-api/playeri/"

@app.route(rvw_route_api_playeri+'get_playeri', methods=['POST'])
def get_playeri():
    return jsonify(rasp=rvw_structuri.Player.getFiles()) 
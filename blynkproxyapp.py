from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BLYNK_BASE_URL = "https://blynk.cloud/external/api"

@app.route('/blynk/<token>/pin/<pin>', methods=['GET'])
def get_blynk_value(token, pin):
    #url = f"{BLYNK_BASE_URL}/get?token={token}&pin={pin}"
    url=f"https://192.168.1.103:9443/get?token={token}&pin={pin}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/blynk/<token>/set/<pin>/<value>', methods=['GET'])
def set_blynk_value(token, pin, value):
    #url = f"{BLYNK_BASE_URL}/update?token={token}&{pin}={value}"
    #url=f"https://192.168.1.103:9443/n4uICWW8guhAulM_Rwe2bG8hjcP3TzMB/update/V1?value=1"
    url=f"https://192.168.1.103:9443/update?token={token}&{pin}={value}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

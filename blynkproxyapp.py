from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BLYNK_BASE_URL = "https://blynk.cloud/external/api"

@app.route('/blynk/<token>/pin/<pin>', methods=['GET'])
def get_blynk_value(token, pin):
    url = f"{BLYNK_BASE_URL}/get?token={token}&pin={pin}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/blynk/<token>/set/<pin>/<value>', methods=['GET'])
def set_blynk_value(token, pin, value):
    url = f"{BLYNK_BASE_URL}/update?token={token}&{pin}={value}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

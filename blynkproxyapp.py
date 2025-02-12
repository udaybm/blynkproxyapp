from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BLYNK_SERVER = "https://192.168.1.103:9443"

@app.route('/blynk/<token>/set/<pin>/<value>', methods=['GET'])
def set_blynk_value(token, pin, value):
    """ Set a virtual pin value in Blynk. """
    success, response_text = set_blynk(BLYNK_SERVER, token, pin, value)

    if success:
        return jsonify({"status": "success", "pin": pin, "value": value, "response": response_text}), 200
    else:
        return jsonify({"status": "error", "message": response_text}), 500


def set_blynk(blynk_server, token, pin, value):
    """ Sends a request to Blynk and handles response. """
    blynk_url = f"{blynk_server}/{token}/update/{pin}?value={value}"

    try:
        response = requests.get(blynk_url, verify=False)  # Disable SSL verification
        response.raise_for_status()

        if response.text.strip() == "":
            return True, f"Value {value} sent successfully to {pin}."
        
        return True, response.text

    except requests.exceptions.RequestException as e:
        return False, str(e)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

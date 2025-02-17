from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

BLYNK_SERVER = "https://192.168.1.103:9443"  # Blynk HTTPS Server

@app.route('/blynk/<token>/set/<pin>/<value>', methods=['GET'])
def set_blynk_value(token, pin, value):
    """ Detect request origin and process accordingly. """
    
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = "android" in user_agent or "iphone" in user_agent or "thunkable" in user_agent

    if request.is_secure:
        print("✅ HTTPS Request Received")
    else:
        print("✅ HTTP Request Received")
    
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


# Function to start the HTTP server (for mobile app)
def run_http():
    app.run(host="0.0.0.0", port=5001, use_reloader=False)  # ⚠️ Remove debug=True

# Function to start the HTTPS server (for Web View)
def run_https():
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'flask.key'), use_reloader=False)  # ⚠️ Remove debug=True

if __name__ == '__main__':
    # Start HTTP & HTTPS servers in separate daemon threads
    http_thread = threading.Thread(target=run_http, daemon=True)
    https_thread = threading.Thread(target=run_https, daemon=True)

    http_thread.start()
    https_thread.start()

    # Keep the main thread alive until interrupted
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down servers...")


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading

# Configuration
BLYNK_SERVER = "https://192.168.1.103:9443"  # Blynk HTTPS Server

# Create two separate Flask apps
app_http = Flask('http_app')
app_https = Flask('https_app')

#Enable CORS for all routes
#https://192.168.1.117:5000/blynk/n4uICWW8guhAulM_Rwe2bG8hjcP3TzMB/set/V1/1
CORS(app_http)
CORS(app_https)

def register_routes(app):
    @app.route('/blynk/<token>/set/<pin>/<value>', methods=['GET'])
    def set_blynk_value(token, pin, value):
        user_agent = request.headers.get('User-Agent', '').lower()
        is_mobile = "android" in user_agent or "iphone" in user_agent or "thunkable" in user_agent

        if request.is_secure:
            print("✅ HTTPS Request Received")
        else:
            print("✅ HTTP Request Received")

        success, response_text = set_blynk(BLYNK_SERVER, token, pin, value)

        if success:
            return jsonify({"status": "success", "pin": pin, "value": value, "response": response_text}), 200
        else:
            return jsonify({"status": "error", "message": response_text}), 500

# Register the route in both apps
register_routes(app_http)
register_routes(app_https)

def set_blynk(blynk_server, token, pin, value):
    blynk_url = f"{blynk_server}/{token}/update/{pin}?value={value}"
    try:
        response = requests.get(blynk_url, verify=False)
        response.raise_for_status()
        if response.text.strip() == "":
            return True, f"Value {value} sent successfully to {pin}."
        return True, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)

# Start each server in its own thread
# Function to start the HTTP server (for mobile app)
def run_http():
    app_http.run(host="0.0.0.0", port=5001, use_reloader=False)
# Function to start the HTTPS server (for Web View)
def run_https():
    app_https.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'flask.key'), use_reloader=False)

if __name__ == '__main__':
    # Start HTTP & HTTPS servers in separate daemon threads
    threading.Thread(target=run_http, daemon=True).start()
    threading.Thread(target=run_https, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down servers...")
#PS D:\prac-python> .\venv-in-cmd1
#(testpkl) D:\AI\esp-test-ml>python d:\prac-python\blynkproxy\blynkproxyser.py  
from flask import Flask, request, jsonify
from main import get_video_info
import os

app = Flask(__name__)

# API Key para autenticación
API_KEY = os.getenv("API_KEY", "@Dsc123456789")

@app.route("/scrape", methods=["POST"])
def scrape_video():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    if not data or "link" not in data:
        return jsonify({"error": "Missing 'link' parameter"}), 400
    
    video_info = get_video_info(data["link"])
    return jsonify(video_info)

if __name__ == "__main__":
    #Para local
    #app.run(host="0.0.0.0", port=5000, debug=True)
    # Para Replit
    #app.run(host="0.0.0.0", port=8080, debug=True)
    # Para Azure
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

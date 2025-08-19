from flask import Flask, request, jsonify
from resume_analyzer import analyze_resume
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Service is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        resume_url = data.get('resume_url')

        status = analyze_resume(resume_url)

        return jsonify({
            "name": name,
            "email": email,
            "mobile": mobile,
            "status": status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render assigns the port via environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

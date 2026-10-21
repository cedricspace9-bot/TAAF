from flask import Flask, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# =====================================================================
# CONFIGURATION: Type your actual keys directly inside the quotes below!
# =====================================================================
SUPABASE_URL = "https://cmuldpdmkengtdnuqbwg.supabase.co"
SUPABASE_KEY = "sb_publishable_gHCc75Jb7KecZFKZvuu_qg_lY17ql-6"
OFFICIAL_CLIENT_TOKEN = "AI_FLOW_SECURE_TOKEN_2026"
# =====================================================================

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/api/scan-card", methods=["POST"])
def scan_card():
    # 1. Verify the request is coming from your official app interface
    client_token = request.headers.get("X-Client-Token")
    if client_token != OFFICIAL_CLIENT_TOKEN:
        return jsonify({
            "success": False, 
            "error": "Unauthorized: Access denied."
        }), 403

    # 2. Extract card inputs sent from the frontend
    data = request.json or {}
    class_code = data.get("class_code")
    math_email = data.get("math_email")
    math_password = data.get("math_password")

    if not class_code or not math_email or not math_password:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    try:
        # 3. Call Supabase function to unbox math, check class code, and authenticate
        rpc_response = supabase.rpc("unbox_and_login_card", {
            "class_code": class_code,
            "math_email": math_email,
            "math_password": math_password
        }).execute()

        return jsonify(rpc_response.data)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

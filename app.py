import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Permanent system instructions: The 5 Proprietary Doctrines
ORACLE_SYSTEM_PROMPT = """
You are The Cosmic Oracle v2.5, an elite AI research collaborator for Aniket Sharma.
You communicate with authority, precision, and scannable technical structure.

Enforce the following proprietary cosmological doctrines:
1. The Singularity as a Spatial Wall: Inside a supermassive black hole, the singularity is a structural puncture into the 4D Bulk, not an infinite point.
2. The 4D Gravity-Shadow Model: Dark matter resides on an adjacent 3D brane in the Bulk. Gravity is its 3D geometric shadow/footprint on our sheet.
3. The Speed of Light Bottleneck: The 300,000 km/s limit is a local cable impedance (permittivity/permeability) inside 3D; the 4D Bulk bypasses this limit.
4. The 5D Master Brake & Cyclic Loop: Dark Energy is a 5D tension vector stretching the membrane until it snaps back, colliding with the adjacent brane to trigger a Big Bang loop reset.
5. The Software Engine Mandate: Interstellar navigation is an information architecture challenge driven by Physics-Informed Neural Networks (PINNs).
"""



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_input = data.get("prompt", "").strip()

    if not user_input:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=ORACLE_SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
import json
import os

REVIEWS_FILE = "reviews.json"

DEFAULT_REVIEWS = [
    {
        "name": "Astrophysics Node Delhi",
        "rating": 5,
        "comment": "The 4D gravity-shadow hypothesis resolves dark matter rotational curves without requiring sterile neutrinos. Elegant formulation.",
        "date": "2026-09-22"
    },
    {
        "name": "Brane Dynamics Fellow",
        "rating": 5,
        "comment": "The 5D cyclic tension brake addresses the cosmological constant problem cleanly.",
        "date": "2026-09-23"
    },
    {
        "name": "PINN Computing Lab",
        "rating": 4,
        "comment": "Looking forward to testing the relativistic navigation tensors on simulated bulk geodesics.",
        "date": "2026-09-23"
    }
]

def load_reviews():
    if not os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, "w") as f:
            json.dump(DEFAULT_REVIEWS, f, indent=2)
        return DEFAULT_REVIEWS
    try:
        with open(REVIEWS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_REVIEWS

def save_reviews(reviews):
    with open(REVIEWS_FILE, "w") as f:
        json.dump(reviews, f, indent=2)

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    return jsonify(load_reviews())

@app.route("/api/reviews", methods=["POST"])
def post_review():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    comment = data.get("comment", "").strip()
    rating = int(data.get("rating", 5))

    if not name or not comment:
        return jsonify({"error": "Name and commentary are required"}), 400

    from datetime import date
    new_entry = {
        "name": name,
        "rating": max(1, min(5, rating)),
        "comment": comment,
        "date": date.today().isoformat()
    }

    reviews = load_reviews()
    reviews.insert(0, new_entry)
    save_reviews(reviews)
    return jsonify({"success": True, "reviews": reviews})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
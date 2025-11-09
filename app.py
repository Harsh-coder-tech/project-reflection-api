from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Store responses in memory
user_responses = []

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Project Reflection API!"})

@app.route("/questions", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")

    filtered = questions
    if category:
        filtered = [q for q in filtered if q["category"].lower() == category.lower()]
    if difficulty:
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]

    return jsonify(filtered)

@app.route("/questions/<int:id>", methods=["GET"])
def get_question_by_id(id):
    for q in questions:
        if q["id"] == id:
            return jsonify(q)
    return jsonify({"error": "Question not found"}), 404

@app.route("/submit", methods=["POST"])
def submit_response():
    data = request.get_json()
    question_id = data.get("id")
    user_answer = data.get("answer", "").strip()
    username = data.get("username", "Anonymous").strip()

    for q in questions:
        if q["id"] == question_id:
            response = {
                "user": username,
                "question": q["question"],
                "your_answer": user_answer
            }
            user_responses.append(response)
            return jsonify({
                "message": "Response recorded successfully.",
                "response": response
            })

    return jsonify({"error": "Question not found"}), 404

@app.route("/responses", methods=["GET"])
def get_all_responses():
    return jsonify(user_responses)

if __name__ == "__main__":
    app.run(debug=True)

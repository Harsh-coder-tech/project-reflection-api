<<<<<<< HEAD
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Load or initialize responses
RESPONSES_FILE = "responses.json"
if os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, "r") as f:
        user_responses = json.load(f)
else:
    user_responses = []

def save_responses():
    with open(RESPONSES_FILE, "w") as f:
        json.dump(user_responses, f, indent=2)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Project Reflection API!"})

@app.route("/questions", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")

    filtered = questions
    if category:
        filtered = [q for q in filtered if q.get("category", "").lower() == category.lower()]
    if difficulty:
        filtered = [q for q in filtered if q.get("difficulty", "").lower() == difficulty.lower()]

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

    question_id = data.get("question_id")
    user_answer = data.get("your_answer", "").strip()
    username = data.get("username", "Anonymous").strip()

    if not question_id or not user_answer:
        return jsonify({"error": "Missing question_id or your_answer"}), 400

    question = next((q for q in questions if q["id"] == question_id), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    response = {
        "question_id": question_id,
        "user": username,
        "question": question["question"],
        "your_answer": user_answer
    }
    user_responses.append(response)
    save_responses()

    return jsonify({
        "message": "Response recorded successfully.",
        "response": response
    })

@app.route("/responses", methods=["GET"])
def get_all_responses():
    return jsonify(user_responses)

@app.route("/response/<int:question_id>", methods=["GET"])
def get_response_by_question_id(question_id):
    matched = [r for r in user_responses if r["question_id"] == question_id]
    if matched:
        return jsonify(matched)
    return jsonify({"error": "No response found for this question ID"}), 404

if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> 927425018716cc1d80ccb68c2391dc705c8bd074

from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_password_strength(password):
    length_error = len(password) < 8
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    digit_error = re.search(r"\d", password) is None
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    feedback = []
    if length_error:
        feedback.append("❌ Must be at least 8 characters long.")
    if uppercase_error:
        feedback.append("❌ Must include at least one uppercase letter.")
    if lowercase_error:
        feedback.append("❌ Must include at least one lowercase letter.")
    if digit_error:
        feedback.append("❌ Must include at least one number.")
    if special_char_error:
        feedback.append("❌ Must include at least one special character (!@#$%^&*(),.?\":{}|<>).")

    errors = sum([length_error, uppercase_error, lowercase_error, digit_error, special_char_error])
    if errors == 0:
        strength = "💪 Strong"
    elif errors <= 2:
        strength = "🙂 Moderate"
    else:
        strength = "😢 Weak"

    return feedback, strength

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = []
    strength = ""
    password = ""
    if request.method == "POST":
        password = request.form["password"]
        feedback, strength = check_password_strength(password)
    return render_template("index.html", feedback=feedback, strength=strength, password=password)

if __name__ == "__main__":
    app.run(debug=True)

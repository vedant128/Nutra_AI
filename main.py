from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import google.generativeai as genai

# Configure the Generative AI API
genai.configure(api_key="AIzaSyDlGsewmGEAytSdQa8CZUjiLvHgo-gO-eA")

# Generative AI model configuration
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


class DailyRoutine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    wakeup_time = db.Column(db.String(50), nullable=False)
    sleep_time = db.Column(db.String(50), nullable=False)
    study_time = db.Column(db.String(50), nullable=False)
    exercise_time = db.Column(db.String(50), nullable=False)
    water_intake = db.Column(db.Integer, nullable=False)
    dietary_preferences = db.Column(db.String(100), default='')
    health_goal = db.Column(db.String(100), default='')


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials, please try again.", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    routine = DailyRoutine.query.filter_by(user_id=user_id).first()
    edit_form = False

    if not routine:
        edit_form = True
    elif request.args.get('edit') == 'True':
        edit_form = True

    if request.method == "POST":
        wakeup_time = request.form.get("wakeup_time")
        sleep_time = request.form.get("sleep_time")
        exercise_time = request.form.get("exercise_time")
        water_intake = request.form.get("water_intake")
        dietary_preferences = request.form.get("dietary_preferences")
        health_goal = request.form.get("health_goal")
        study_time = request.form.get("study_time")

        if routine:
            routine.wakeup_time = wakeup_time
            routine.sleep_time = sleep_time
            routine.exercise_time = exercise_time
            routine.water_intake = water_intake
            routine.dietary_preferences = dietary_preferences
            routine.health_goal = health_goal
            routine.study_time = study_time
        else:
            routine = DailyRoutine(
                user_id=user_id,
                wakeup_time=wakeup_time,
                sleep_time=sleep_time,
                exercise_time=exercise_time,
                water_intake=water_intake,
                dietary_preferences=dietary_preferences,
                health_goal=health_goal,
                study_time=study_time,
            )
            db.session.add(routine)

        db.session.commit()
        flash("Daily routine saved successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", routine=routine, edit_form=edit_form)


@app.route("/expert", methods=["GET", "POST"])
def expert():
    if "user_id" not in session:
        flash("Please log in to access this page.", "danger")
        return redirect(url_for("login"))

    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["msg"]
    return generate_response(user_message)


# Function to generate a chatbot response
history = []


def generate_response(user_input):
    user_id = session.get("user_id")
    if not user_id:
        return "Please log in to continue."

    user = User.query.get(user_id)
    routine = DailyRoutine.query.filter_by(user_id=user_id).first()

    if not routine or not routine.dietary_preferences or not routine.health_goal:
        return "Please update your dietary preferences and health goal in the dashboard."

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
            f"You are an expert named NutraAI that integrates physical and mental health management. "
            f"Provide personalized advice to {user.username} on diet, exercise, sleep, and stress. "
            f"This user is a {routine.dietary_preferences} and is working on a goal of {routine.health_goal}. "
            f"Provide concise, direct advice in no more than 3-4 lines."
            f"and you have to only answer health and wellbeing and you do not ans remaining questions"
            f"and you have to only answer health and wellbeing and you do not ans remaining questions"
        ),
    )

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Update history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return model_response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

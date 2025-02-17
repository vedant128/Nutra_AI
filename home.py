# Program to implement a chatbot:
import google.generativeai as genai
from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Chatbot part:
genai.configure(api_key="AIzaSyDlGsewmGEAytSdQa8CZUjiLvHgo-gO-eA")

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


# CREATE DATABASE
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Adding Flask:
app = Flask(__name__)
app.config['SECRET_KEY'] = "Ilikeyoumarfii"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db.init_app(app)

# Table creation:
class UserDB(db.Model):
    id:Mapped[int] = mapped_column(Integer,primary_key = True,autoincrement = True)
    email: Mapped[str] = mapped_column(String)
    name:Mapped[str] = mapped_column(String)
    age:Mapped[int] = mapped_column(Integer)
    diet:Mapped[str] = mapped_column(String)
    goal:Mapped[float] = mapped_column(String)

with app.app_context():
    db.create_all()


# Logging In:
@app.route("/",methods = ["GET","POST"])
def login():
    global model
    if request.method == "POST":
        record = db.session.execute(db.select(UserDB).where(UserDB.email == request.form.get("email"))).scalar()
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            system_instruction=f"\nYou are an expert and your name is NutraAI that integrates physical and mental health management. Your task is to provide personalized advice to {record.name} on diet, exercise, sleep, and stress, and this user is a {record.diet} and on a goal on {record.goal}.Provide concise, direct advice with no more than 3-4 lines",
        )
        return redirect(url_for("home"))
    return render_template("index.html")

# Signing Up:
@app.route("/signup",methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        user = UserDB(
            name = request.form.get("name"),
            email = request.form.get("email"),
            age = request.form.get("age"),
            diet = request.form.get("dietary_preferences"),
            goal =request.form.get("health_goal")
        )
        db.session.add(user)
        db.session.commit()
    return render_template("index.html")

# Chatting:
@app.route("/home")
def home():
    return render_template("chat.html")

# Chat route to handle user input:
@app.route("/get", methods=["GET","POST"])
def chat():
    user_message = request.form["msg"]
    return generate_response(user_message)

# Function to generate a chatbot response
history = []
def generate_response(user_input):
    global model
    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(user_input)
    model_response = response.text
    print(model_response)
    # Appending History:
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})
    return f"{model_response.replace('*', '')}"

if __name__ == "__main__":
    app.run(debug = True)
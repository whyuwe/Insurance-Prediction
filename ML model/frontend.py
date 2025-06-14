# app.py (Flask App)

from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_session import Session
import requests
from forms.LoginForm import LoginForm ,SignForm 
from forms.PredictionForm import PredictionForm
app = Flask(__name__)
app.config["SECRET_KEY"] = "yuvi is secret key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

API_URL = "http://localhost:8000/predict"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Homie")

@app.route("/about")
def about():
    if "user_name" not in session:
        flash("Login Required")
        return redirect(url_for("login", next=request.url))
    else:
        flash(f"Hi {session['user_name']}, have a good day")
    return render_template("about.html", title="About")

@app.route("/contact")
def contact():
    if "user_name" not in session:
        flash("Login Required", "danger")
        return redirect(url_for("login", next=request.url))

    flash(f"Hi {session['user_name']}, have a good day!", "success")
    return render_template("contact.html", title="Contact")

@app.route("/signup")
def signup():
    return render_template("signup.html", title="SignUp")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["user_name"] = form.username.data
        flash(f"Successfully logged in as {session['user_name'].title()}!")
        next_url = request.args.get("next")
        return redirect(next_url or url_for("home"))

    return render_template("login.html", title="Login", form=form)

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    prediction = None
    confidence = None
    probabilities = None

    if form.validate_on_submit():
        input_data = {
            "age": form.age.data,
            "weight": form.weight.data,
            "height": form.height.data,
            "income_lpa": form.income_lpa.data,
            "smoker": form.smoker.data,
            "city": form.city.data,
            "occupation": form.occupation.data
        }

        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()
            if response.status_code == 200 and "predicted_category" in result:
                prediction = result["predicted_category"]
                flash(f"Prediction: {prediction}", "success")
            else:
                flash("API Error: Could not get prediction.", "danger")
        except requests.exceptions.RequestException:
            flash("Could not connect to the prediction server.", "danger")

    return render_template("predict.html", title="Predict", form=form,
                           prediction=prediction, confidence=confidence, probabilities=probabilities)

if __name__ == "__main__":
    app.run(debug=True)

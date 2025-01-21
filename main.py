from base64 import b64decode
import os
import random
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine

SPRINT = 3
APP = Flask(__name__)

@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )

@APP.route("/data", methods=["GET"])
def data():
    if SPRINT < 1:
        return render_template("data.html")

    db = Database("Monster")
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )

@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")

    db = Database("Monster")
    df = db.dataframe()

    options = df.columns.tolist()
    x_axis = request.values.get("x_axis") or options[0]
    y_axis = request.values.get("y_axis") or options[1]
    target = request.values.get("target") or options[-1]

    graph = chart(
        df=df,
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )

@APP.route("/model", methods=["GET", "POST"])
def model():
    try:
        print("Accessing /model route...")
        db = Database('Monster')
        print("Database initialized.")

        options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
        filepath = os.path.join("app", "model.joblib")
        retrain = request.values.get("retrain") == "on"
        print(f"Retrain selected: {retrain}")

        if not os.path.exists(filepath) or retrain:
            print("Training new model...")
            df = db.dataframe()
            print(f"DataFrame columns: {df.columns}")
            machine = Machine(df[options])
            machine.save(filepath)
            print("Model trained and saved.")
        else:
            print("Loading model from file...")
            machine = Machine.open(filepath)
            print("Model loaded successfully.")

        stats = [round(random.uniform(1, 250), 2) for _ in range(3)]
        level = request.values.get("level", type=int) or random.randint(1, 20)
        health = request.values.get("health", type=float) or stats.pop()
        energy = request.values.get("energy", type=float) or stats.pop()
        sanity = request.values.get("sanity", type=float) or stats.pop()
        print(f"Input values - Level: {level}, Health: {health}, Energy: {energy}, Sanity: {sanity}")

        features = DataFrame([dict(zip(options[:-1], (level, health, energy, sanity)))])
        print(f"Prediction features: {features}")
        prediction, confidence = machine(features)
        print(f"Prediction: {prediction}, Confidence: {confidence}")

        info = machine.info()
        return render_template(
            "model.html",
            info=info,
            level=level,
            health=health,
            energy=energy,
            sanity=sanity,
            prediction=prediction,
            confidence=f"{confidence:.2%}",
        )
    except Exception as e:
        print("Error in /model route:", str(e))
        return render_template(
            "model.html",
            info=None,
            error=f"An error occurred: {str(e)}"
        )



if __name__ == '__main__':
    APP.run(debug=True)

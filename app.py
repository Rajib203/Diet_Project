# app.py (FULL) — Advanced pipeline model + BMI chart + Food Recommendations

from flask import Flask, render_template, request
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# ✅ Load advanced pipeline model
payload = pickle.load(open("model_advanced.pkl", "rb"))
model_pipe = payload["pipeline"]
meta = payload.get("meta", {})
accuracy = meta.get("test_accuracy", None)


def get_food_recommendations(prediction: str):
    """
    Returns list of foods to eat based on predicted diet type text.
    Works with labels like:
    'High Protein ...', 'Low Calorie ...', 'Low Carb ...', 'Balanced ...'
    """
    p = (prediction or "").lower()

    if "high protein" in p:
        return [
            "Eggs", "Chicken breast", "Paneer / Tofu",
            "Greek yogurt / Curd", "Dal / Lentils", "Nuts & seeds"
        ]

    if "low calorie" in p:
        return [
            "Salad (cucumber, tomato, carrots)", "Vegetable soup",
            "Grilled/roasted vegetables", "Oats / Dalia",
            "Fruits (apple, papaya)", "Sprouts"
        ]

    if "low carb" in p:
        return [
            "Eggs", "Fish / Chicken", "Paneer / Tofu",
            "Avocado (optional)", "Leafy greens (spinach)", "Nuts (limit)"
        ]

    if "balanced" in p:
        return [
            "Roti / Rice (controlled portion)", "Dal",
            "Seasonal vegetables", "Curd / Milk",
            "Fruits", "Nuts (small portion)"
        ]

    # fallback
    return [
        "Whole grains", "Lean protein", "Vegetables",
        "Fruits", "Healthy fats", "Plenty of water"
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    bmi_category = None
    chart_path = None
    foods = []

    if request.method == "POST":
        # Get inputs
        age = int(request.form["age"])
        gender = request.form["gender"]
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        activity = request.form["activity"]
        goal = request.form["goal"]
        region = request.form["region"]

        # ✅ BMI
        bmi = weight / ((height / 100) ** 2)

        # BMI category
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        # ✅ Prepare input for pipeline
        X_input = pd.DataFrame([{
            "Age": age,
            "Gender": gender,
            "Height_cm": height,
            "Weight_kg": weight,
            "BMI": bmi,
            "Activity_Level": activity,
            "Goal": goal,
            "Region": region
        }])

        # ✅ Predict
        prediction = model_pipe.predict(X_input)[0]

        # ✅ Food recommendations
        foods = get_food_recommendations(prediction)

        # ✅ BMI chart
        if not os.path.exists("static"):
            os.makedirs("static")

        chart_path = "static/bmi_chart.png"
        plt.figure(figsize=(5, 3.2))
        plt.bar(["Your BMI"], [bmi])
        plt.axhline(18.5, linestyle="--")
        plt.axhline(25, linestyle="--")
        plt.axhline(30, linestyle="--")
        plt.title("BMI Health Chart")
        plt.ylabel("BMI")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

    return render_template(
        "index.html",
        prediction=prediction,
        bmi_category=bmi_category,
        chart_path=chart_path,
        accuracy=accuracy,
        foods=foods
    )


if __name__ == "__main__":
    app.run(debug=True)
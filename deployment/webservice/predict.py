import pickle
import pandas as pd
from flask import Flask, request, jsonify

with open("model.pkl", "rb") as f_in:
    model = pickle.load(f_in)


def prepare_features(event):
    # Convert to data frame
    data = pd.DataFrame([event])
    data.columns = [c.lower().replace(" ", "_") for c in data.columns]
    return data


def predict(features):
    preds = model.predict(features)
    return preds[0]


app = Flask("diabetes-prediction")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    event = request.get_json()
    print(f"Received event: {event}")  # Debugging line

    features = prepare_features(event)
    print(f"Prepared features: {features}")  # Debugging line

    preds = predict(features)
    result = {"outcome": int(preds)}
    print(f"Prediction result: {result}")  # Debugging line

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)

import pandas as pd
import mlflow
from mlflow import MlflowClient
from flask import Flask, request, jsonify

uri = "http://localhost:5001"
mlflow.set_tracking_uri(uri=uri)
mlflow.set_experiment("diabetes")
client = MlflowClient(tracking_uri=uri)
logged_model = client.get_model_version_by_alias("diabetes_model", "champion")
run_id = logged_model.run_id

model = mlflow.pyfunc.load_model(logged_model.source)


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
    result = {"outcome": int(preds), "model_version": str(run_id)}
    print(f"Prediction result: {result}")  # Debugging line

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)

from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, "rt", encoding="utf-8") as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text("data.b64")

    actual_result = model.base64_decode(base64_input)

    expected_result = {
        "data": {
            "Pregnancies": 0,
            "Glucose": 131,
            "BloodPressure": 0,
            "SkinThickness": 0,
            "Insulin": 0,
            "BMI": 43.2,
            "DiabetesPedigreeFunction": 0.27,
            "Age": 26,
        },
        "patient_id": "256",
    }

    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)

    patient_data = {
        "Pregnancies": 0,
        "Glucose": 131,
        "BloodPressure": 0,
        "SkinThickness": 0,
        "Insulin": 0,
        "BMI": 43.2,
        "DiabetesPedigreeFunction": 0.27,
        "Age": 26,
    }

    actual_features = model_service.prepare_features(patient_data)
    print(actual_features)
    expected_fetures = {
        "pregnancies": 0,
        "glucose": 131,
        "bloodpressure": 0,
        "skinthickness": 0,
        "insulin": 0,
        "bmi": 43.2,
        "diabetespedigreefunction": 0.27,
        "age": 26,
    }

    assert actual_features == expected_fetures


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock)

    features = {
        "pregnancies": 0,
        "glucose": 131,
        "bloodPressure": 0,
        "skinThickness": 0,
        "insulin": 0,
        "bmi": 43.2,
        "diabetespedigreefunction": 0.27,
        "age": 26,
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction


def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = "Test123"
    model_service = model.ModelService(model_mock, model_version)

    base64_input = read_text("data.b64")

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        "predictions": [
            {
                "model": "prima-diabetes-prediction-model",
                "version": model_version,
                "prediction": {
                    "outcome": 10.0,
                    "patient_id": "256",
                },
            }
        ]
    }

    assert actual_predictions == expected_predictions

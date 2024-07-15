import requests

event = {
    "Pregnancies": 0,
    "Glucose": 131,
    "BloodPressure": 0,
    "SkinThickness": 0,
    "Insulin": 0,
    "BMI": 43.2,
    "DiabetesPedigreeFunction": 0.27,
    "Age": 26,
}
url = "http://localhost:9696/predict"

response = requests.post(url, json=event)
print(response.json())

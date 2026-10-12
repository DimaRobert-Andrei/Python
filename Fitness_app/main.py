import os
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

APP_KEY_ID = os.getenv("NIX_APP_ID")
X_APP_KEY_ID = os.getenv("NIX_API_KEY")
SHEETY_API = os.getenv("SHEETY_ENDPOINT")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")

USER_INPUT = input("Exercise description?\n")

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_KEY_ID,
    "x-app-key": X_APP_KEY_ID,
}
app_endpoint = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"

informations = {
    "query": USER_INPUT,
    "weight_kg": 72,
    "height_cm": 178,
    "age": 22,
    "gender": "male",
}
try:
    response = requests.post(url=app_endpoint, headers=headers, json=informations)
    result = response.json()

    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    headers_sheety = {
        "Authorization": SHEETY_AUTH,
     }

    for exercises in result["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercises["name"].title(),
                "duration": exercises["duration_min"],
                "calories": exercises["nf_calories"],
            }
        }

        response_sheety = requests.post(
            url=SHEETY_API, headers=headers_sheety, json=sheet_inputs
        )
        print("Răspuns Sheety:", response_sheety.text)
except requests.exceptions.HTTPError as http_err:
    print(f"Eroare HTTP / Autentificare: {http_err}")
    print("Detalii de la server:", response.text)

except KeyError as err:
    print(f"Eroare de structură (KeyError): Nu s-a găsit cheia {err} în răspuns.")
    print("Răspuns primit de la server:", result)

except Exception as err:
    print(f"A apărut o eroare neașteptată: {err}")
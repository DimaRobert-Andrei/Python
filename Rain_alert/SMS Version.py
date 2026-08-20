import requests
from twilio.rest import Client

ACCOUNT_SID = "-"
AUTH_TOKEN = "-"
TWILIO_NUMBER = "+-"
MY_PHONE = "+-"

APP_ID = "-"


LAT = 44.856850
LON = 24.869740

params = {
    "appid": APP_ID,
    "lat": LAT,
    "lon": LON,
    "cnt": 8,
}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast", params=params
)
response.raise_for_status()
weather_data = response.json()

rain_hours = []
weather_description = ""

for item in weather_data["list"]:
    condition_code = item["weather"][0]["id"]
    time_of_forecast = item["dt_txt"]
    description = item["weather"][0]["description"]

    if int(condition_code) < 700:
        rain_hours.append(time_of_forecast)
        weather_description = description

if rain_hours:
    alert_message = (
        f"🚨 ALERTĂ METEO: Se anunță {weather_description} în Pitești! "
        f"A strâns cineva rufele de pe sârmă sau a luat umbrela? "
        f"Primele semne apar la ora: {rain_hours[0]}."
    )


client = Client(ACCOUNT_SID, AUTH_TOKEN)
message = client.messages.create(
    to=MY_PHONE, from_=TWILIO_NUMBER, body=alert_message
)

print(f"Mesaj trimis cu succes! Status: {message.status}")

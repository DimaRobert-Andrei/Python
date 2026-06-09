

import requests
import yaml
import time
import smtplib
import ssl
from email.message import EmailMessage




class ApiDataFetcher:


    def __init__(self, config):
        self.location = config.get("LOCATION_QUERY")
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

        if not self.location:
            print("EROARE: Te rog setează 'LOCATION_QUERY' în config.py!")
            self.location = None

    def get_coordinates(self):

        params = {'name': self.location, 'count': 1}
        try:
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            if response.status_code != 200: return None, None
            data = response.json()
            if not data.get('results'): return None, None
            lat = data['results'][0]['latitude']
            lon = data['results'][0]['longitude']
            print(f"[API INFO] Locație găsită: {self.location} -> Lat: {lat}, Lon: {lon}")
            return lat, lon
        except Exception as e:
            print(f"[API EROARE GEO] O eroare a apărut la preluarea coordonatelor: {e}")
            return None, None

    def read_data(self):

        if not self.location: return None, None, None
        lat, lon = self.get_coordinates()
        if lat is None or lon is None: return None, None, None
        temp, umid, pm25 = None, None, None
        try:
            params_weather = {'latitude': lat, 'longitude': lon, 'current': 'temperature_2m,relative_humidity_2m'}
            response_weather = requests.get(self.weather_url, params=params_weather, timeout=10)
            if response_weather.status_code == 200:
                data_weather = response_weather.json()
                temp = data_weather.get('current', {}).get('temperature_2m')
                umid = data_weather.get('current', {}).get('relative_humidity_2m')
                print(f"[API VREME SUCCES] Temp: {temp}, Umid: {umid}")
            else:
                print(f"[API EROARE VREME] Status: {response_weather.status_code}")
        except Exception as e:
            print(f"[API EROARE VREME] O eroare a apărut: {e}")
        try:
            params_air = {'latitude': lat, 'longitude': lon, 'current': 'pm2_5'}
            response_air = requests.get(self.air_quality_url, params=params_air, timeout=10)
            if response_air.status_code == 200:
                data_air = response_air.json()
                pm25 = data_air.get('current', {}).get('pm2_5')
                print(f"[API POLUARE SUCCES] PM2.5: {pm25}")
            else:
                print(f"[API EROARE POLUARE] Status: {response_air.status_code}")
        except Exception as e:
            print(f"[API EROARE POLUARE] O eroare a apărut: {e}")
        if temp is not None and umid is not None and pm25 is not None:
            print(f"[API SUCCES FINAL] Date reale: Temp={temp}, Umid={umid}, PM2.5={pm25}")
            return float(temp), float(umid), float(pm25)
        else:
            print("[API EROARE] Datele nu au putut fi preluate complet (Vremea sau Poluarea au eșuat).")
            return None, None, None


class EmailService:

    def __init__(self, host, port, sender, password):
        self.host = host
        self.port = int(port)
        self.sender = sender
        self.password = password

    def send_alert(self, subject, recipient, plain_text_body, html_body=None):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg.set_content(plain_text_body)
        if html_body:
            msg.add_alternative(html_body, subtype='html')
        context = ssl.create_default_context()
        try:
            print(f"[EMAIL] Încercare conexiune SSL la {self.host} pe portul {self.port}...")
            with smtplib.SMTP_SSL(self.host, self.port, context=context, timeout=10) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)
                print("[EMAIL] Alertă Email trimisă cu succes!")
        except smtplib.SMTPException as e:
            print(f"[EMAIL] Eroare SMTP: {e}")
        except Exception as e:
            print(f"[EMAIL] Eroare la trimiterea Email-ului (SSL): {e}")


class BlynkService:

    def __init__(self, auth_token, api_url="https://blynk.cloud/external/api/update"):
        self.auth_token = auth_token
        self.api_url = api_url

    def send_data(self, data):

        try:
            params = {
                'token': self.auth_token,
                'V1': data['temperatura']['valoare'],
                'V2': data['umiditate']['valoare'],
                'V3': data['pm2_5']['valoare']

            }
            print(f"[BLYNK DEBUG] Se trimit: V1={params['V1']}, V2={params['V2']}, V3={params['V3']}")
            response = requests.get(self.api_url, params=params, timeout=5)
            if response.status_code == 200:
                print("[BLYNK] Date trimise cu succes la Blynk (Status 200).")
            else:
                print(f"[BLYNK] ️ Eroare REALĂ la trimitere: {response.status_code} | Mesaj: {response.text}")
        except Exception as e:
            print(f"[BLYNK]  Eroare generală: {e}")


class YamlLogger:


    def __init__(self, filename):
        self.filename = filename

    def log(self, data):
        try:
            with open(self.filename, 'a') as f:
                yaml.dump([data], f, allow_unicode=True, default_flow_style=False)
            print(f"[YAML] Date salvate în '{self.filename}'")
        except Exception as e:
            print(f"[YAML] Eroare la salvarea fișierului: {e}")



class DataProcessor:


    def __init__(self, email_service, email_recipient):
        self.email_service = email_service
        self.email_recipient = email_recipient
        self.alert_sent = False

    def process_data(self, temp, umid, pm25):

        if temp < 18:
            temp_desc = "Prea Rece"
        elif 19 <= temp <= 25:
            temp_desc = "Confortabil (Ideal)"
        elif temp > 26:
            temp_desc = "Prea Cald"
        else:
            temp_desc = "Neutru"


        if umid < 30:
            umid_desc = "Prea Uscat"
        elif 40 <= umid <= 60:
            umid_desc = "Ideal (Confortabil)"
        elif umid > 70:
            umid_desc = "Prea Umed"
        else:
            umid_desc = "Acceptabil"


        if 0 <= pm25 <= 12.0:
            pm25_desc = "Bun"
        elif 12.1 <= pm25 <= 35.4:
            pm25_desc = "Moderat"
        elif 35.5 <= pm25 <= 55.4:
            pm25_desc = "Nociv (pt. grupuri sensibile)"
        elif 55.5 <= pm25 <= 150.4:
            pm25_desc = "Nociv"
        elif pm25 > 150.5:
            pm25_desc = "Foarte Nociv"
        else:
            pm25_desc = "Indefinit"


        if pm25 >= 35.5:
            if not self.alert_sent:
                print("[ALERTA] Prag Nociv detectat! Trimitere Email...")

                plain_text_content = f"""
                *** A fost detectată o alertă de sănătate! ***

                Calitatea aerului a depășit pragul de siguranță.

                RAPORT DE STARE:
                - Calitate Aer (PM2.5): {pm25} µg/m³ (Nivel: {pm25_desc})
                - Temperatură: {temp}°C (Nivel: {temp_desc})
                - Umiditate: {umid}% (Nivel: {umid_desc})

                Vă rugăm luați măsurile necesare.
                """

                html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                        .container {{ width: 90%; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                        .header {{ font-size: 24px; color: #d9534f; /* Roșu pentru alertă */ }}
                        .content {{ margin-top: 20px; }}
                        .alert-message {{ font-size: 18px; font-weight: bold; color: #d9534f; }}
                        table {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
                        th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
                        th {{ background-color: #f4f4f4; }}
                        .label {{ font-weight: bold; }}
                        .value-alert {{ font-weight: bold; color: #d9534f; }}
                        .footer {{ margin-top: 20px; font-size: 12px; color: #888; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1 class="header">Notificare Alertă Sistem IoT</h1>
                        <div class="content">
                            <p class="alert-message">Atenție! A fost detectată o alertă de sănătate.</p>
                            <p>Sistemul de monitorizare a calității aerului a înregistrat o valoare care depășește pragul de siguranță. Vă prezentăm mai jos raportul complet al senzorilor:</p>

                            <table>
                                <tr>
                                    <th>Parametru</th>
                                    <th>Valoare Înregistrată</th>
                                    <th>Nivel de Confort/Calitate</th>
                                </tr>
                                <tr>
                                    <td class="label">🌡Temperatură</td>
                                    <td>{temp}°C</td>
                                    <td>{temp_desc}</td>
                                </tr>
                                <tr>
                                    <td class="label"> Umiditate</td>
                                    <td>{umid}%</td>
                                    <td>{umid_desc}</td>
                                </tr>
                                <tr>
                                    <td class="label"> Calitate Aer (PM2.5)</td>
                                    <td class="value-alert">{pm25} µg/m³</td>
                                    <td class="value-alert">{pm25_desc}</td>
                                </tr>
                            </table>

                            <p class="footer">
                                Acesta este un mesaj automat trimis de sistemul de monitorizare TST-RO.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """


                self.email_service.send_alert(
                    subject=f"ALERTA Aer Nociv: PM2.5 la {pm25} µg/m³",
                    recipient=self.email_recipient,
                    plain_text_body=plain_text_content,
                    html_body=html_content
                )
                self.alert_sent = True
        else:
            if self.alert_sent:
                print("[INFO] Calitatea aerului a revenit la normal.")
                self.alert_sent = False


        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'temperatura': {'valoare': temp, 'nivel': temp_desc},
            'umiditate': {'valoare': umid, 'nivel': umid_desc},
            'pm2_5': {'valoare': pm25, 'nivel': pm25_desc}
        }







class IotApplication:


    def __init__(self, config):
        self.config = config
        self.delay = config["LOOP_DELAY_SECONDS"]


        self.sensor = ApiDataFetcher(config)
        self.email_service = EmailService(
            config["EMAIL_HOST"],
            config["EMAIL_PORT"],
            config["EMAIL_SENDER"],
            config["EMAIL_PASSWORD"]
        )
        self.processor = DataProcessor(
            self.email_service,
            config["EMAIL_RECIPIENT"]
        )
        self.blynk_service = BlynkService(
            config["BLYNK_AUTH_TOKEN"],
            config["BLYNK_API_URL"]
        )
        self.yaml_logger = YamlLogger(config["YAML_FILE"])

    def _display_report(self, data):
        """Afișează raportul formatat în consolă."""
        print("--- RAPORT PROCESAT ---")
        print(f"  Temperatură: {data['temperatura']['valoare']}°C ({data['temperatura']['nivel']})")
        print(f"  Umiditate:   {data['umiditate']['valoare']}% ({data['umiditate']['nivel']})")
        print(f"  Calit. Aer:  {data['pm2_5']['valoare']} µg/m³ ({data['pm2_5']['nivel']})")
        print("-------------------------")

    def run(self):
        """Rulează bucla principală a aplicației."""
        print("Sistem de monitorizare IoT pornit. (Ctrl+C pentru a opri)")

        while True:
            try:
                temp, umid, pm25 = self.sensor.read_data()

                if temp is None or umid is None or pm25 is None:
                    print(f"[INFO] Preluarea datelor a eșuat. Se așteaptă {self.delay} secunde...")
                    time.sleep(self.delay)
                    con tinue

                processed_data = self.processor.process_data(temp, umid, pm25)
                self._display_report(processed_data)
                self.blynk_service.send_data(processed_data)
                self.yaml_logger.log(processed_data)

                print(f"[INFO] Următoarea actualizare în {self.delay} secunde.")
                time.sleep(self.delay)

            except KeyboardInterrupt:
                print("\nOprire program.")
                break
            except Exception as e:
                print(f"A apărut o eroare necunoscută în bucla principală: {e}")
                time.sleep(10)
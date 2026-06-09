
import sys



try:
    import requests
    import yaml
except ImportError:
    print("EROARE: Bibliotecile necesare nu sunt instalate.")
    print("Rulează: pip install requests pyyaml")
    sys.exit(1)
from config import CONFIG
from iot_system import IotApplication


def main():

    if CONFIG["BLYNK_AUTH_TOKEN"].startswith("eTpqan"):
        print("Token-ul Blynk este setat.")
    else:
        print("!!! ATENȚIE: Nu ai setat BLYNK_AUTH_TOKEN în config.py! Oprește și editează.")
        return

    if CONFIG["EMAIL_PASSWORD"] == "xxxx yyyy zzzz wwww":
        print("!!! ATENȚIE: Nu ai setat EMAIL_PASSWORD în config.py! Alerta nu va funcționa.")

    print("Inițializare aplicație IoT...")
    app = IotApplication(CONFIG)
    app.run()

if __name__ == "__main__":
    main()

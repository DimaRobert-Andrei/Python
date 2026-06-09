

import smtplib
from email.message import EmailMessage
import sys

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_SENDER = "proiectiot2025@gmail.com"  # <--- MODIFICĂ
EMAIL_PASSWORD = "anzbdicykgezwxiw"  # <--- MODIFICĂ (parola pt. aplicații)
EMAIL_RECIPIENT = "proiectiot2025@gmail.com"  # <--- MODIFICĂ

print("Încercare de conectare la serverul Gmail...")

try:
    # Creare mesaj
    msg = EmailMessage()
    msg.set_content("Acesta este un email de test.")
    msg['Subject'] = "Test Python SMTP"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    # Conectare la serverul SMTP
    # Adăugăm un timeout de 10 secunde
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10)
    server.set_debuglevel(1)
    print("\n--- Începere conexiune TLS ---")
    server.starttls()  # Securizare conexiune
    print("\n--- Conexiune TLS stabilită ---")

    print("\n--- Încercare autentificare ---")
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print("\n--- Autentificare reușită ---")

    # Trimitere email
    server.send_message(msg)
    print("\n--- Email de test trimis cu succes! ---")

    server.quit()
    print("\n--- Deconectat de la server ---")

except Exception as e:
    print(f"\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"!!! A APĂRUT O EROARE !!!")
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"Eroarea este: {e}")
    sys.exit(1)
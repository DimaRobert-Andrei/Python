import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

try:
    import requests
    import yaml
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Eroare Import",
                         "Bibliotecile necesare nu sunt instalate.\nRulează: pip install requests pyyaml")
    sys.exit(1)


try:
    from config import CONFIG
    from iot_system import IotApplication
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Eroare Config", f"Nu am putut importa modulele locale:\n{e}")
    sys.exit(1)


class TextRedirector(object):


    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.see("end")  # Auto-scroll
        self.widget.configure(state="disabled")

    def flush(self):
        pass


class IotGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT System Control Panel")
        self.root.geometry("600x450")
        self.app_running = False
        self.iot_app_instance = None

        # --- Zona de Status Configurare ---
        self.frame_status = tk.LabelFrame(root, text="Status Configurare", padx=10, pady=10)
        self.frame_status.pack(fill="x", padx=10, pady=5)

        # Label Token
        self.lbl_token = tk.Label(self.frame_status, text="Verificare Token Blynk...", font=("Arial", 10, "bold"))
        self.lbl_token.pack(anchor="w")

        # Label Email
        self.lbl_email = tk.Label(self.frame_status, text="Verificare Parolă Email...", font=("Arial", 10, "bold"))
        self.lbl_email.pack(anchor="w")

        # --- Zona de Log-uri (Consola) ---
        self.frame_logs = tk.LabelFrame(root, text="Log-uri Sistem", padx=10, pady=10)
        self.frame_logs.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_logs = scrolledtext.ScrolledText(self.frame_logs, height=10, state='disabled', bg="#f0f0f0")
        self.txt_logs.pack(fill="both", expand=True)

        # Redirecționăm stdout (print) către fereastra de text
        sys.stdout = TextRedirector(self.txt_logs)
        # Opțional: redirecționăm și stderr pentru erori
        sys.stderr = TextRedirector(self.txt_logs)

        # --- Zona de Butoane ---
        self.frame_controls = tk.Frame(root, padx=10, pady=10)
        self.frame_controls.pack(fill="x")

        self.btn_start = tk.Button(self.frame_controls, text="PORNEȘTE SISTEMUL", bg="#4CAF50", fg="white",
                                   font=("Arial", 12, "bold"), command=self.start_iot_thread)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=5)

        self.btn_exit = tk.Button(self.frame_controls, text="IEȘIRE", bg="#f44336", fg="white",
                                  font=("Arial", 12, "bold"), command=self.on_close)
        self.btn_exit.pack(side="right", fill="x", expand=True, padx=5)

        self.check_config()

    def check_config(self):

        if CONFIG["BLYNK_AUTH_TOKEN"].startswith("eTpqan"):
            self.lbl_token.config(text="✓ Token Blynk setat corect", fg="green")
            token_ok = True
        else:
            self.lbl_token.config(text="⚠ ATENȚIE: BLYNK_AUTH_TOKEN incorect/nesetat!", fg="red")
            print("!!! ATENȚIE: Nu ai setat BLYNK_AUTH_TOKEN în config.py!")
            token_ok = False

        if CONFIG["EMAIL_PASSWORD"] == "xxxx yyyy zzzz wwww":
            self.lbl_email.config(text="⚠ ATENȚIE: Parolă Email default!", fg="orange")
            print("!!! ATENȚIE: Nu ai setat EMAIL_PASSWORD! Alerta nu va funcționa.")
        else:
            self.lbl_email.config(text="✓ Parolă Email setată (format aparent corect)", fg="green")

        if not token_ok:
            self.btn_start.config(state="disabled", bg="#cccccc")

    def start_iot_thread(self):
        self.btn_start.config(state="disabled", text="Sistemul Rulează...")
        self.app_running = True


        t = threading.Thread(target=self.run_iot_logic, daemon=True)
        t.start()

    def run_iot_logic(self):
        print("Inițializare aplicație IoT...")
        try:
            self.iot_app_instance = IotApplication(CONFIG)
            self.iot_app_instance.run()
        except Exception as e:
            print(f"EROARE CRITICĂ în execuție: {e}")
            self.root.after(0, lambda: self.btn_start.config(state="normal", text="PORNEȘTE SISTEMUL"))

    def on_close(self):
        print("Se închide aplicația...")
        self.root.destroy()
        sys.exit(0)


def main():
    root = tk.Tk()
    app = IotGuiApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
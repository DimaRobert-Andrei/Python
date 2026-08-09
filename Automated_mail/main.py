import smtplib
import datetime as dt
import pandas as pd
import random

letter1="letter_templates\\letter_1.txt"
letter2="letter_templates\\letter_2.txt"
letter3="letter_templates\\letter_3.txt"

file="birthdays.csv"
day=dt.date.today()
df= pd.read_csv(file)
month_now=day.month
day_now=day.day
Name=df["name"]
month=df["month"]
day_birth=df["day"]
mail_destinatar=df["email"]
for nume, luna, ziua in zip(Name, month, day_birth):
    if month_now == luna and day_now == ziua:
        lista_scrisori=[letter1, letter2, letter3]
        fisier_ales=random.choice(lista_scrisori)
        with open(fisier_ales, 'r') as continut_ales:
            continut=continut_ales.read()
        nume_schimbat= continut.replace("[NAME]",nume)

my_email = "dimarobert788@gmail.com"
password = "vubc awyd rfed oiid"
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    email_body = f"Subject: La multi ani!\n\n{nume_schimbat}"
    connection.sendmail(from_addr=my_email,to_addrs=mail_destinatar,msg=email_body.encode('utf-8'))

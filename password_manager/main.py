from tkinter import *
from tkinter import messagebox
import random
import string
Pink="#e2979c"
Red="#e7305b"
Green="#9bdeac"
Yellow="#f7f5dd"
Font_name="Times New Roman"
def save_text():
    mail=text_mail.get()
    parola=password_text.get()
    website=website_text.get()
    if len(website) == 0 or len(parola) == 0 or len(mail) == 0:
        messagebox.showwarning(title="Atenție!", message="Te rog nu lăsa niciun câmp gol!")
    else:
        este_ok = messagebox.askokcancel(title=website,message=f"Acestea sunt datele introduse:\n\nEmail: {mail}\nParolă: {parola}\n\nDorești să le salvezi?")
    if este_ok:
        with open("data.txt","a") as file:
            file.write(mail+" |")
            file.write(parola+" |")
            file.write(website+"|")
            file.write("\n")
        print("Salvat cu succes!")
    password_text.delete(0, END)
    website_text.delete(0, END)

def generate_text():
    caractere_dorite = "$#!?"
    lungime_dorita=10
    litere_mari=string.ascii_uppercase
    litere_mici=string.ascii_lowercase
    generate_password = [random.choice(caractere_dorite),
                         random.choice(litere_mari),
                         random.choice(litere_mici),
                         random.choice(string.digits)]
    toate_caracterele= litere_mici + caractere_dorite + litere_mari+string.digits


    for _ in range(lungime_dorita):
        generate_password.append(random.choice(toate_caracterele))
    random.shuffle(generate_password)
    rezultat="".join(generate_password)
    password_text.insert(0,rezultat)

window=Tk()
window.title("Password Manager")
canvas=Canvas(window,width=200,height=200,bg=Yellow,highlightthickness=0)
image=PhotoImage(file="logo1.png")
canvas.create_image(0,0,image=image,anchor=NW)
window.config(padx=20,pady=20,bg=Yellow)
text_mail=Entry(window,  width = 50)
canvas.grid(row=1,column=2)

website_text=Entry(window, width = 50)
website_text.grid(row=2,column=2,columnspan=2)
website_label=Label(window, text="Website:",bg=Yellow)
website_label.grid(row=2,column=1,)
website_text.focus()
text_mail.grid(row=3,column=2,columnspan=2)
email_label=Label(window, text="Email Address:",bg=Yellow)
email_label.grid(row=3,column=1)
text_mail.insert(0,"dimarobert778@gmail.com")
password_label=Label(window, text="Password:",bg=Yellow)
password_label.grid(row=4,column=1)
password_text=Entry(window,  width = 32,show="*")
password_text.grid(row=4,column=2)
button_generate=Button(text="Generate Password")
button_generate.configure(width=14,activebackground=Green,relief=RIDGE,command=generate_text)
button_generate.grid(row=4,column=3,columnspan=2)
button_add=Button(text="Add Password")
button_add.configure(width=60,activebackground=Green,relief=RIDGE,command=save_text)
button_add.grid(row=5,column=1,columnspan=3)





window.mainloop()
from tkinter import *
from tkinter import messagebox
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pw_letters = [random.choice(letters) for _ in range(nr_letters)]
    pw_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    pw_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = pw_symbols + pw_numbers + pw_letters

    random.shuffle(password_list)
    password = "".join(password_list)

    pw_entry.insert(0, password)
    if len(password) > 1:
        pw_entry.delete(0, END)
        pw_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = pw_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
                  }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Opps", message="Please make sure any fields are not empty")

    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the detail:\nEmail: {email}\nPassword: {password}\nIs "
                                               f"it okay?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                pw_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_pass():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
pw_img = PhotoImage(file="logo.png")
canvas.create_image(110, 100, image=pw_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username")
email_label.grid(column=0, row=2)

pw_label = Label(text="Password")
pw_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "ggwp@gmail.com")

pw_entry = Entry(width=34)
pw_entry.grid(column=1, row=3, padx=10)

# Buttons
pw_gen_button = Button(text="Generate Password", command=gen_pass)
pw_gen_button.grid(column=2, row=3)

add_button = Button(text="Add", width=14, command=save)
add_button.grid(column=1, row=4)

search_button = Button(text="Search", width=12, command=find_pass)
search_button.grid(column=2, row=1)

window.mainloop()

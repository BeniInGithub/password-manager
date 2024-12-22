from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_input.get()
    email_input_value = email_input.get()
    password_input_value = password_input.get()
    new_data = {
        website: {
            "email": email_input_value,
            "password": password_input_value,
        }
    }

    if len(website) == 0 or len(password_input_value) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        try:
            with open("passwords.json", mode="r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except(FileNotFoundError, json.decoder.JSONDecodeError):
            with open('passwords.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)

            with open("passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- Search password  ------------------------------- #

def search():
    key = website_input.get()
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)

            if key in data:
                email = data[key]["email"]
                password = data[key]["password"]
                messagebox.showinfo(
                    title=key,
                    message=f"Email: "
                            f"{email} \n Password: {password}")
            else:
                messagebox.showinfo(
                    title="Error",
                    message="No details for this website exists."
                )

    except FileNotFoundError:
        messagebox.showinfo(
        title="Error",
        message="No Data File Found."
    )


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

##labels

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

##inputs
website_input = Entry(width=21)
website_input.grid(column=1, row=1)
website_input.focus()
email_input = Entry(width=38)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, "beni@email.com")
password_input = Entry(width=21)
password_input.grid(column=1, row=3)

##buttons
search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
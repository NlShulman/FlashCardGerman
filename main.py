import csv
import json
import random
import time
from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox

import pandas

BACKGROUND_COLOR = "#B1DDC6"


# ---------------------------- WORDS LIST ------------------------------- #
all_words = pandas.read_csv("ge-en.csv")
words = {word.German: word.English for (index, word) in all_words.iterrows()}
german = ""
english = ""
unknown_words = {}


def generate_random_word():
    global german, english, flip_timer, words
    window.after_cancel(flip_timer)
    german, english = random.choice(list(words.items()))
    canvas.itemconfig(card_title, text="German")
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(word, text=f"{german}")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(word, text=english)


def know():
    global words
    del words[german]
    header = ["German", "English"]
    data_items = words.items()
    data_list = list(data_items)
    df = pandas.DataFrame(data_list)
    df.to_csv("ge-en.csv", header=header, index=False)
    canvas.itemconfig(word, text=f"{german}")
    generate_random_word()


def dont_know():
    canvas.itemconfig(word, text=f"{german}")
    unknown_words[german] = english
    try:
        with open("unknown_words.txt", mode= "r") as df:
            data = json.load(df)
    except JSONDecodeError:
        with open("password_manager.json", mode="w") as df:
            json.dump(unknown_words, df, indent=4)
    except FileNotFoundError:
        with open("unknown_words.txt", mode="w") as df:
            json.dump(unknown_words, df, indent=4)
    else:
        data.update(unknown_words)
        with open("unknown_words.txt", mode="w") as df:
            json.dump(data, df, indent=4)
    generate_random_word()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Learn German")
window.configure(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

front_image = PhotoImage(file="card_front.png")
back_image = PhotoImage(file="card_back.png")
canvas = Canvas(width=800, height=530, background=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 270, image=front_image)
canvas.grid(row=0, column=0, columnspan=2, pady=20)

card_title = canvas.create_text(400, 100, text="German", fill="black", font=("Courier", 20, "bold"))
word = canvas.create_text(400, 300, fill="black", font=("Courier", 65, "bold"))

no_image_button = PhotoImage(file="wrong.png")
no_button = Button(image=no_image_button, width=70, height=70, highlightthickness=0)
no_button.configure(command=dont_know)
no_button.grid(column=0, row=2)

yes_image_button = PhotoImage(file="right.png")
yes_button = Button(image=yes_image_button, width=70, height=70, highlightthickness=0)
yes_button.configure(command=know)
yes_button.grid(column=1, row=2)


generate_random_word()



window.mainloop()

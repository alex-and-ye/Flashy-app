from tkinter import *
import pandas as pd
from random import choice
BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- UNPACKING WORD LIST ------------------------------- #

library = pd.read_csv("data/french_words.csv")
library = pd.DataFrame(library).to_dict(orient="records")

try:
    known_words = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    known_words = pd.DataFrame(library)
finally:
    known_words = known_words.to_dict(orient="records")
# ---------------------------- PICKING RANDOM FRENCH WORD ------------------------------- #
random_card = {}


def get_random_word():
    global flip_timer, random_card
    window.after_cancel(flip_timer)
    random_card = choice(known_words)
    canvas.itemconfig(card_img, image=card_front)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=random_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


# ---------------------------- FLIPPING CARD AFTER 3 SEC ------------------------------- #

def flip_card():
    canvas.itemconfig(card_img, image=card_back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=random_card["English"], fill="white")

# ---------------------------- CASE WHEN USER KNOWS THE WORD ------------------------------- #


def known_word():
    global random_card, known_words
    known_words = [item for item in known_words if item.get("French") != random_card["French"]]
    if len(known_words) != 0:
        get_random_word()
    else:
        known_words = library
        get_random_word()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=card_front)

language = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=get_random_word)
unknown_button.grid(row=1, column=0)

correct_image = PhotoImage(file="images/right.png")
known_button = Button(image=correct_image, highlightthickness=0, command=known_word)
known_button.grid(row=1, column=1)

get_random_word()

window.mainloop()

pd.DataFrame(known_words).to_csv('data/words_to_learn.csv')

from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
current_card = {}
to_learn = {}

try:  # Checks if the file is already in the folder
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:  # This deals with any failures
    original_data = pandas.read_csv("data/katakana_list.csv")  # Makes the csv file readable
    to_learn = original_data.to_dict(orient="records")  # Orient makes it a list of dictionaries
else:  # If there are no issues, then this is executed
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def right_card():
    to_learn.remove(current_card)  # Removes this card from the csv file
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)  # overrides csv file
    next_card()


# Sets up the window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Flips the card after 3 seconds
flip_timer = window.after(3000, flip_card)

# Sets up the canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")  # canvases allow us to layer things
card_back_img = PhotoImage(file="images/card_back.png")  # canvases allow us to layer things
card_background = canvas.create_image(400, 263, image=card_front_img)  # on top of each other
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)

# Sets up the "right" button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_card)
right_button.grid(row=1, column=0)

# Sets up the "wrong" button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=1)

# Starts the program
next_card()

# Let's the window stay on the screen
window.mainloop()

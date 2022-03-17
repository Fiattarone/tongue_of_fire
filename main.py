from tkinter import *
from tkinter import messagebox
import pandas
from language_locker import LanguageLocker
import random
import json

BACKGROUND_COLOR = "#B1DDC6"
game_select = 0
card_flip_delay = 10
current_lang = []
language_enigma = LanguageLocker()
current_score = 0
study = []
complete_exit = False


# Answered correct
def correct_answer():
    global current_score
    current_score += 1
    next_card()
    # record correct answer, increase score


# Answered incorrect
def wrong_answer():
    # record incorrect answer
    new_data = {
        "English": current_lang[0],
        list(current_lang[1].keys())[0].title(): current_lang[1][list(current_lang[1].keys())[0]]
    }
    study.append(new_data)
    next_card()


# Card Actions
def flip_card_to_back(lang_pack):
    canvas.itemconfig(current_card_image, image=card_back_img)
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(body_text, text=lang_pack[0])


def next_card():
    global current_lang
    global language_enigma
    canvas.itemconfig(current_card_image, image=card_front_img)
    print("summon next card")
    language_enigma = random.choice(language_list)
    current_lang = language_enigma.select_random_from_locker((french_checked_state.get(),
                                                              italian_checked_state.get(), spanish_checked_state.get()))
    canvas.itemconfig(title_text, text=list(current_lang[1].keys())[0].title())
    canvas.itemconfig(body_text, text=current_lang[1][list(current_lang[1].keys())[0]])
    window.after(card_flip_delay, flip_card_to_back, current_lang)

# Radio Button Manager
def radio_used():
    print(f"Switched radio {radio_state.get()}")


# Continue to game
def continue_to_game():
    # global italian_checked_state, french_checked_state, spanish_checked_state
    # print(italian_checked_state, french_checked_state, spanish_checked_state)
    if italian_checked_state.get() == 1 or french_checked_state.get() == 1 or spanish_checked_state.get() == 1:
        global game_select
        global card_flip_delay
        # mode_chosen = True
        game_select = radio_state.get()
        card_flip_delay = int(seconds_to_answer.get())*1000
        print(game_select)
        # print(mode_chosen)
        game_mode1.destroy()
        game_mode2.destroy()
        continue_button.destroy()
        window.destroy()
    else:
        messagebox.showinfo("Error: Select Language", "Please select at least one language to continue.")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            with open("Study/words_to_study.csv", "r") as study_these:
                data = json.load(study_these)
        except FileNotFoundError:
            with open("Study/words_to_study.csv", "w") as study_these:
                json.dump(study, study_these, indent=4)
        else:
            # print(data.update(study))
            # data.update(study)
            with open("Study/words_to_study.csv", "w") as study_these:
                json.dump(study, study_these, indent=4)
        finally:
            window.destroy()


def on_closing_options():
    global complete_exit
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        complete_exit = True
        window.destroy()


# UI
window = Tk()
window.title("Startup Options")
window.config(padx=100, pady=100, bg=BACKGROUND_COLOR)

# TODO: The crazy one
# TODO: Show total score
# Choose game mode
radio_state = IntVar()
game_mode1 = Radiobutton(text="Learning Mode", value=1, variable=radio_state, command=radio_used)
game_mode2 = Radiobutton(text="Twister Mode", value=2, variable=radio_state, command=radio_used)
radio_state.set(1)
game_mode1.grid(column=1, row=0)
game_mode2.grid(column=1, row=1)

# Select languages
italian_checked_state = IntVar(value=1)
spanish_checked_state = IntVar()
french_checked_state = IntVar()

select1 = Checkbutton(text="Italian", variable=italian_checked_state)
select2 = Checkbutton(text="Spanish", variable=spanish_checked_state)
select3 = Checkbutton(text="French", variable=french_checked_state)
# select1.setvar(italian_checked_state, 1)
select1.grid(column=0, row=2)
select2.grid(column=1, row=2)
select3.grid(column=2, row=2)

# Select time to answer
spinbox_label = Label(text="Seconds", justify="right")
spinbox_label.grid(column=0, row=3)
seconds_to_answer = Spinbox(from_=1, to=10, width=5)
seconds_to_answer.grid(column=1, row=3)

# Continue button
continue_button = Button(text="Continue", fg="black", bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=1, padx=3,
                         pady=3, command=continue_to_game)
continue_button.grid(column=1, row=4)
# options loop
window.protocol("WM_DELETE_WINDOW", on_closing_options)
window.mainloop()

if not complete_exit:
    # TODO: dynamically program languages, so users can load whatever languages they want from the csv
    # TODO: Fix later so that it doesn't use so much data, only load necessary data
    # Load language data
    language_data = pandas.read_csv("./data/languages.csv")
    language_list = [LanguageLocker(en=x.values[1],
                                    it=x.values[2],
                                    fr=x.values[0],
                                    es=x.values[3]) for idx, x in language_data.iterrows()]

    # New window
    window = Tk()
    window.title("Romantic Language Twister")
    window.config(padx=45, pady=45, bg=BACKGROUND_COLOR)

    # Create Canvas
    canvas = Canvas(width=1000, height=600, highlightthickness=0)
    canvas.config(bg=BACKGROUND_COLOR)
    canvas.grid(row=0, column=0, columnspan=2)
    card_front_img = PhotoImage(file="./images/card_front.png")
    card_back_img = PhotoImage(file="./images/card_back.png")
    right_img = PhotoImage(file="./images/right.png")
    wrong_img = PhotoImage(file="./images/wrong.png")
    current_card_image = canvas.create_image(500, 300, image=card_front_img)
    title_text = canvas.create_text(500, 170, text="Press A Button", fill="black", font=("Ariel", 60, "italic"))
    body_text = canvas.create_text(500, 290, text="To Begin", fill="black", font=("Ariel", 80, "bold"))

    right_button = Button(image=right_img, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, padx=3, pady=3,
                          command=correct_answer)
    right_button.grid(row=1, column=0)

    wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, padx=3, pady=3,
                          command=wrong_answer)
    wrong_button.grid(row=1, column=1)

    # flashcard loop
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

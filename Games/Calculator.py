import customtkinter as ctk

root = ctk.CTk()

root.title("Calculator")

ctk.set_appearance_mode("dark")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

task_bar_height = 50
window_height = screen_height - task_bar_height

root.geometry(f"{screen_width}x{window_height}+0+0")


# Make columns equal

for i in range(4):
    root.columnconfigure(i, weight=1)

for i in range(7):
    root.rowconfigure(i, weight=1)


equation = ""


# ---------- FUNCTIONS ----------

def update_display():

    display.configure(state="normal")

    display.delete(0, ctk.END)

    display.insert(0, equation)

    display.configure(state="readonly")


def press(value):

    global equation

    equation += value

    update_display()


def clear():

    global equation

    equation = ""

    update_display()


def backspace():

    global equation

    equation = equation[:-1]

    update_display()


def calculate():

    global equation

    try:

        equation = str(eval(equation))

        update_display()

    except:

        equation = ""

        display.configure(state="normal")

        display.delete(0, ctk.END)

        display.insert(0, "Error")

        display.configure(state="readonly")


# ---------- TITLE ----------

title = ctk.CTkLabel(
    root,
    text="Calculator",
    font=("Arial", 40)
)

title.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=20
)


# ---------- DISPLAY ----------

display = ctk.CTkEntry(
    root,
    font=("Arial", 35),
    justify="right",
    state="readonly"
)

display.grid(
    row=1,
    column=0,
    columnspan=4,
    padx=40,
    pady=20,
    sticky="ew"
)


# ---------- BUTTONS ----------

buttons = [
    ("%", 2, 0),
    ("CE", 2, 1),
    ("C", 2, 2),
    ("⌫", 2, 3),

    ("7", 3, 0),
    ("8", 3, 1),
    ("9", 3, 2),
    ("÷", 3, 3),

    ("4", 4, 0),
    ("5", 4, 1),
    ("6", 4, 2),
    ("×", 4, 3),

    ("1", 5, 0),
    ("2", 5, 1),
    ("3", 5, 2),
    ("−", 5, 3),

    ("0", 6, 0),
    (".", 6, 1),
    ("=", 6, 2),
    ("+", 6, 3)
]


for text, row, column in buttons:

    if text == "C" or text == "CE":

        command = clear

    elif text == "⌫":

        command = backspace

    elif text == "÷":

        command = lambda: press("/")

    elif text == "×":

        command = lambda: press("*")

    elif text == "−":

        command = lambda: press("-")

    elif text == "=":

        command = calculate

    elif text == "%":

        command = lambda: press("%")

    else:

        command = lambda x=text: press(x)


    button = ctk.CTkButton(
        root,
        text=text,
        font=("Arial", 25),
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="nsew"
    )


root.mainloop()
import customtkinter as ctk
import time
import random

time_taken = 0
game_active = True
valid_click = False
start_time = 0
test_running = False

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Reaction Time Tester")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

task_bar_height = 50
window_height = screen_height - task_bar_height

root.geometry(f"{screen_width}x{window_height}+0+0")


title = ctk.CTkLabel(
    root,
    text="REACTION TIME TESTER",
    font=("Arial", 40)
)
title.pack()


instructions = ctk.CTkLabel(
    root,
    text="Click when the text changes!\nThe text will change between 1 to 5 seconds!",
    font=("Arial", 20)
)
instructions.pack(pady=20)


def start_test():
    global start_time, valid_click, test_running

    valid_click = False
    test_running = True

    start_button.configure(state="disabled")
    the_button.configure(state="normal")

    wait_time = random.randint(1, 5)

    instructions.configure(text="Get ready...")

    root.after(wait_time * 1000, show_click_button)


def show_click_button():
    global start_time, valid_click

    if test_running:
        start_time = time.time()
        valid_click = True

        instructions.configure(text="CLICK NOW!")


def end_test():
    global valid_click, test_running

    if not test_running:
        return

    test_running = False
    the_button.configure(state="disabled")

    if valid_click:
        reaction_time = time.time() - start_time

        instructions.configure(
            text=f"Your reaction time was {reaction_time:.4f} seconds!"
        )

        valid_click = False
        start_button.configure(state="normal")
        start_button.configure(text="Try Again")

    else:
        instructions.configure(
            text="Too early! You must wait for the signal."
        )

        valid_click = False
        start_button.configure(state="normal")
        start_button.configure(text="Try Again")


start_button = ctk.CTkButton(
    root,
    text="Start",
    font=("Arial", 20),
    height=60,
    width=150,
    command=start_test
)

start_button.pack(pady=20)


the_button = ctk.CTkButton(
    root,
    text="CLICK ME",
    font=("Arial", 20),
    height=300,
    width=500,
    state="disabled",
    command=end_test
)

the_button.pack(pady=20)


root.mainloop()
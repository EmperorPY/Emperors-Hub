# Import customtkinter — a modern wrapper around tkinter with nicer widgets
import customtkinter as ctk
# Import random so we can pick a random motivational quote
import random
from playsound3 import playsound
import os
import json
# Set the whole app to dark mode (dark background, light text)
ctk.set_appearance_mode("dark")

# Create the main application window
root = ctk.CTk()
# Set the window title bar text
root.title("LockIn")

script_dir = os.path.dirname(os.path.abspath(__file__))

# ---- Full screen minus task bar ----
# Ask Windows (or whatever OS) how wide the screen is, in pixels
screen_width = root.winfo_screenwidth()
# Ask how tall the screen is, in pixels
screen_height = root.winfo_screenheight()
# We subtract this so the window doesn't hide behind the OS taskbar
task_bar_height = 60
# Place the window: full width, height minus taskbar, at position (0,0) = top-left
root.geometry(f"{screen_width}x{screen_height - task_bar_height}+0+0")

# ---- Timer state ----
# Work phase lasts 25 minutes = 1500 seconds
WORK_SECONDS = 25 * 60
# Rest phase lasts 5 minutes = 300 seconds
REST_SECONDS = 5 * 60
# How many seconds are left in the current countdown; starts at 25:00
remaining = WORK_SECONDS
# Which phase we're in right now: "work" or "rest"; starts as work
phase = "work"
# Whether the timer is currently counting down
running = False
# The ID returned by root.after() so we can cancel the pending tick when pausing/resetting
after_id = None

# ---- Grid: let content fill the whole window ----
# Column 0 = the timer side (left); weight=1 means it grows when the window grows
root.grid_columnconfigure(0, weight=1)
# Column 1 = the motivation side (right); also grows equally
root.grid_columnconfigure(1, weight=1)
# Row 0 = title row; weight=0 means it stays at its natural (fixed) height
root.grid_rowconfigure(0, weight=0)
# Row 1 = the big center block; weight=1 = takes all leftover vertical space
root.grid_rowconfigure(1, weight=1)
# Row 2 = footer row; fixed height
root.grid_rowconfigure(2, weight=0)

# ---- Title ----
# The big "LockIn" heading at the very top
title = ctk.CTkLabel(root, text="LockIn", font=("Helvetica", 70, "bold"))
# Put it in row 0, column 0, with some top/bottom padding
title.grid(row=0, column=0, pady=(30, 10))

# ---- Center block (holds everything else) ----
# An invisible container that holds all the timer widgets (its background is see-through)
center = ctk.CTkFrame(root, fg_color="transparent")
# Place it in row 1, column 0, and let it stretch in all directions
center.grid(row=1, column=0, sticky="nsew")
# Make its single column stretch to fill its width
center.grid_columnconfigure(0, weight=1)
# Give all 5 rows equal stretch weight so things space out vertically
for r in range(5):
    center.grid_rowconfigure(r, weight=1)

# A short descriptive paragraph about what the app does
description = ctk.CTkLabel(
    center,
    text=("LockIn is a clean, distraction-free desktop study timer. "
          "It uses the proven Pomodoro technique (25 minutes of focused work "
          "followed by a 5-minute break) to help you build concentration and avoid burnout."),
    wraplength=700,           # wrap long text at 700 pixels
    font=("Helvetica", 20),
)
# Place it in row 0 of the center frame
description.grid(row=0, column=0, pady=10)

# A label that says "Work Time" or "Rest Time" depending on the current phase
time_type = ctk.CTkLabel(center, text="Work Time", font=("Helvetica", 40))
# Row 1 of the center frame
time_type.grid(row=1, column=0, pady=10)

# The huge countdown display; starts at 25:00
time_display = ctk.CTkLabel(center, text="25:00", font=("Helvetica", 120, "bold"))
# Row 2 of the center frame
time_display.grid(row=2, column=0, pady=10)

# A frame to hold the Start and Reset buttons side-by-side
button_frame = ctk.CTkFrame(center, fg_color="transparent")
# Row 3 of the center frame
button_frame.grid(row=3, column=0, pady=20)

# The Start/Pause/Resume button — clicking it toggles the timer
start_button = ctk.CTkButton(button_frame, text="Start", width=160, height=50, text_color="black", hover_color="green", fg_color="white",
                             font=("Helvetica", 20), command=lambda: toggle())
# Pack it on the left side of the button frame
start_button.pack(side="left", padx=10)

# The Reset button — clicking it stops the timer and resets to 25:00 work
reset_button = ctk.CTkButton(button_frame, text="Reset", width=160, height=50, fg_color = "white", text_color="black", hover_color="red",
                             font=("Helvetica", 20), command=lambda: reset())
# Pack it on the left side too (after Start, so it appears on the right)
reset_button.pack(side="left", padx=10)


def fmt(seconds):
    """Format seconds as MM:SS."""
    # // is integer division → gives minutes; % gives leftover seconds
    # :02d pads with a leading zero so "5" becomes "05"
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def tick():
    """One second has passed — update the countdown."""
    # These variables are declared global because we reassign them here
    global remaining, phase, after_id
    # Subtract one second from the countdown
    remaining -= 1
    # If the countdown has reached zero (or gone below), switch phases
    if remaining <= 0:
        if phase == "work":
            if os.path.exists("LockIn.wav"): # Checks if sound exists
                playsound("LockIn.wav") # Plays it if it does
            # Work just ended → switch to rest
            phase = "rest"
            remaining = REST_SECONDS
            # Change the "Work Time" label to "Rest Time" and make it green
            time_type.configure(text="Rest Time", text_color="green")
        else:
            # Rest just ended → switch back to work
            phase = "work"
            if os.path.exists("LockIn.wav"): # Checks if sound exists
                playsound("LockIn.wav") # Plays it if it does
            remaining = WORK_SECONDS
            # Change the label back to "Work Time" and make it white
            time_type.configure(text="Work Time", text_color="white")
    # Update the on-screen countdown text
    time_display.configure(text=fmt(remaining))
    # Schedule the next tick one second from now — but only if still running
    if running:
        after_id = root.after(1000, tick)


def toggle():
    """Start/pause the timer."""
    # Declare globals because we reassign them
    global running, after_id
    if running:
        # We're currently running → PAUSE
        running = False
        # Cancel the scheduled next tick so it doesn't fire after we paused
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None
        # Change button label from "Pause" to "Resume"
        start_button.configure(text="Resume")
    else:
        # We're paused → START or RESUME
        running = True
        # Change button label from "Start"/"Resume" to "Pause"
        start_button.configure(text="Pause")
        # Schedule the first tick in 1 second (recursion handles the rest)
        after_id = root.after(1000, tick)


def reset():
    """Stop and reset to the beginning of a work phase."""
    # Declare globals because we reassign them
    global running, phase, remaining, after_id
    # Stop the timer
    running = False
    # Cancel any pending tick so it doesn't fire later
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    # Go back to the work phase
    phase = "work"
    # Reset the countdown to 25:00
    remaining = WORK_SECONDS
    # Reset the phase label to "Work Time" with white text
    time_type.configure(text="Work Time", text_color="white")
    # Update the big countdown display
    time_display.configure(text=fmt(remaining))
    # Change the Start button text back to "Start"
    start_button.configure(text="Start")


# ---- Footer ----
# A small gray motivational tagline at the bottom of the window
footer = ctk.CTkLabel(root, text="Focus. Break. Repeat.",
                      font=("Helvetica", 16), text_color="gray")
# Place it in the footer row (row 2)
footer.grid(row=2, column=0, pady=20)

# The right-side frame that holds the "Motivate Me!" section.
# It has a white border, very rounded corners (90px), a set width, and a huge height.
motivate_frame = ctk.CTkFrame(root, border_width=2, corner_radius=90, width=400, height=1000, border_color="white")
# Prevent its children from shrinking it (keeps the fixed 400×1000 size)
motivate_frame.propagate(False)
# Place it in row 1, column 1 (the right-side grid cell)
motivate_frame.grid(row=1, column=1, pady=20)

# A "Tired?" heading inside the motivation frame
motivative_label = ctk.CTkLabel(motivate_frame, text="Tired?", font=("Helvetica", 40))
# Pack it at the top of the frame
motivative_label.pack(pady=10)

def random_quote():
    quotes_file = os.path.join(script_dir, "quotes.json")
    with open(quotes_file, "r") as f:
        quotes = json.load(f)
    return random.choice(quotes)
# The "Motivate Me!" button. When clicked, it updates phrase_label with a random quote.
motivate_button = ctk.CTkButton(motivate_frame, text="Motivate Me!", text_color="black", command=lambda: phrase_label.configure(text=random_quote(), text_color="white", font=("Arial", 15), wraplength=300,), fg_color="white", hover_color="lightgrey")
# Pack the button inside the motivation frame
motivate_button.pack(pady=10)

# A label that will display the chosen quote. Starts empty until the button is clicked.
phrase_label = ctk.CTkLabel(motivate_frame, text="")
# Pack it so it's actually visible on screen (this is essential!)
phrase_label.pack()

# Start the app's main event loop — keeps the window open and responsive
root.mainloop()
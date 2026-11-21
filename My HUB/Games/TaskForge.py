# Import customtkinter (a modern wrapper around tkinter with nicer widgets)
import customtkinter as ctk

# Set the app to dark mode for a more eye-friendly look
ctk.set_appearance_mode("dark")

# Create the main application window
app = ctk.CTk()
# Set the text shown in the window's title bar
app.title("TaskForge")
# Set the window size (500 wide x 700 tall) and position it at the top-left corner (0,0)
app.geometry("500x700+0+0")

# List that holds all the ACTIVE (not yet completed) tasks
tasks = []
# Counter that tracks how many tasks have been completed so far
tasks_completed = 0
# List that holds all tasks that have been marked as completed
completed_tasks = []

# ---------------- GRID CONFIGURATION ----------------
# Make columns/rows stretch so the layout fills the window nicely.
# Column 0 = left side (input frame + active task list).
# weight=1 means it grows when the window is resized; uniform="col" makes
# both columns the same width.
app.grid_columnconfigure(0, weight=1, uniform="col")   # left column (input + active list)
# Column 1 = right side (counter frame + completed task list).
app.grid_columnconfigure(1, weight=1, uniform="col")   # right column (counter + completed)
# Row 0 = title row. weight=0 means it stays at its natural size (doesn't stretch).
app.grid_rowconfigure(0, weight=0)                     # title row (fixed)
# Row 1 = the input/counter row at the top. Fixed height.
app.grid_rowconfigure(1, weight=0)                     # top row: input/counter (fixed)
# Row 2 = the two scrollable task lists. weight=1 means it takes all leftover space.
app.grid_rowconfigure(2, weight=1)                     # middle: task lists (stretch)
# Row 3 = the bottom instructions row. Fixed height.
app.grid_rowconfigure(3, weight=0)                     # bottom: instructions (fixed)

# ---------------- TITLE ----------------
# The big "TaskForge" label at the very top of the window
title = ctk.CTkLabel(
    app,
    text="TaskForge",       # text shown
    font=("Helvetica", 40), # font and size
    text_color="cyan"       # colored text
)
# Place it in row 0, spanning both columns, with top padding, aligned to the top (north)
title.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

# ---------------- INPUT FRAME (top-left) ----------------
# A bordered box that will hold the text entry and the warning label
input_frame = ctk.CTkFrame(
    app,
    width=245,
    height=100,
    border_width=2,         # 2-pixel border
    border_color="cyan"     # border color
)
# Place it in row 1, column 0 (left side), with padding, stretching to fill its cell
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Prevent children from shrinking the frame (keeps the frame's set size)
input_frame.grid_propagate(False)   # keep fixed size

# The text box where the user types a new task
input_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter a task..."   # ghost text when empty
)
# Pack it inside the frame near the top with a little vertical padding
input_entry.pack(pady=10)

# A small label used to show a warning message (e.g. "Please enter a task!")
warning = ctk.CTkLabel(input_frame, text="")
# Pack it under the entry
warning.pack()

# ---------------- COUNTER FRAME (top-right) ----------------
# A bordered box on the right side that displays how many tasks are completed
counter_frame = ctk.CTkFrame(
    app,
    width=200,
    height=100,
    border_width=2,
    border_color="cyan"
)
# Place it in row 1, column 1 (right side), stretching to fill its cell
counter_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
# Keep the counter frame's size fixed even when children would resize it
counter_frame.grid_propagate(False)

# The label inside the counter frame that shows the completed-task text
count_display = ctk.CTkLabel(
    counter_frame,
    text="No Tasks Completed",   # shown initially
    font=("Helvetica", 16),
    wraplength=150               # wrap long text at 150 pixels
)
# Pack it inside the counter frame
count_display.pack(pady=2)

# ---------------- ACTIVE TASK LIST (middle-left) ----------------
# A scrollable frame (middle-left) that lists all active tasks
list_frame = ctk.CTkScrollableFrame(
    app,
    width=220,
    height=400,
    border_width=2,
    border_color="cyan"
)
# Place it in row 2, column 0 (below the input frame), stretching in all directions
list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# ---------------- COMPLETED TASKS (middle-right) ----------------
# A scrollable frame (middle-right) that lists all completed tasks
completed_frame = ctk.CTkScrollableFrame(
    app,
    width=175,
    height=403,
    border_width=2,
    border_color="cyan"
)
# Place it in row 2, column 1 (below the counter), stretching in all directions
completed_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# The header label inside the completed frame
completed = ctk.CTkLabel(
    completed_frame,
    text="Completed Tasks",
    font=("Helvetica", 16),
    wraplength=150
)
# Pack it at the top of the completed frame
completed.pack(pady=2)

# ---------------- INSTRUCTIONS (bottom) ----------------
# A label at the bottom of the window showing the app's tagline
instructions = ctk.CTkLabel(
    app,
    text="Upload, Do, Track, TaskForge.",
    font=("Helvetica", 25),
    text_color="cyan"
)
# Place it in row 3, spanning both columns, aligned to the bottom (south)
instructions.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="s")


# This function deletes an active task and refreshes the list display.
# "item" is the text of the task we want to remove.
def remove_task(item):
    # Remove the task from the active tasks list
    tasks.remove(item)
    # Rebuild the on-screen list so the removed task disappears
    refresh_list()


# This function rebuilds the active task list UI from scratch.
# We clear everything and re-add each task as a new row.
def refresh_list():
    # Clear existing task rows (destroy every child widget in the list frame)
    for widget in list_frame.winfo_children():
        widget.destroy()

    # Rebuild active tasks — one row per task
    for item in tasks:
        # A horizontal row that holds the label + buttons for one task
        row = ctk.CTkFrame(list_frame)
        # Pack it to fill the full width of the list frame
        row.pack(fill="x", pady=2)

        # The task's text label
        label = ctk.CTkLabel(
            row,
            text=item,
            font=("Helvetica", 14),
            wraplength=75   # wrap long tasks at 75 pixels
        )
        # Place on the left side of the row
        label.pack(side="left", padx=10, pady=5)

        # The "X" button that removes this task
        remove_button = ctk.CTkButton(
            row,
            text="❌",
            width=30,
            fg_color="transparent",         # invisible background
            hover_color="darkred",          # turns dark red on hover
            # Use default arg i=item so each button remembers its own task
            command=lambda i=item: remove_task(i)
        )
        # Place on the right side of the row
        remove_button.pack(side="right", padx=5)

        # The "✔" button that marks this task complete
        mark_button = ctk.CTkButton(
            row,
            text="✔️",
            width=30,
            fg_color="transparent",
            hover_color="darkgreen",        # turns dark green on hover
            command=lambda i=item: mark_complete(i)
        )
        # Also on the right (before the X button, since both use side="right")
        mark_button.pack(side="right", padx=5)


# This function rebuilds the completed tasks UI from scratch.
def refresh_completed():
    # Clear existing completed rows — but keep the "Completed Tasks" header label
    for widget in completed_frame.winfo_children():
        if widget != completed:
            widget.destroy()

    # Update completed counter heading (kept the same text; could be dynamic)
    completed.configure(text="Completed Tasks")

    # Rebuild completed task rows — one per completed task
    for item in completed_tasks:
        # A horizontal row for one completed task
        row = ctk.CTkFrame(completed_frame)
        row.pack(fill="x", pady=2)

        # The completed task's text label
        label = ctk.CTkLabel(
            row,
            text=item,
            font=("Helvetica", 14),
            wraplength=100  # wrap at 100 pixels
        )
        label.pack(padx=10, pady=5)


# This function moves a task from the active list to the completed list.
def mark_complete(item):
    # We're modifying tasks_completed, so declare it as global
    global tasks_completed

    # Remove from active tasks and add to completed tasks
    tasks.remove(item)
    completed_tasks.append(item)
    # Increment the completed-tasks counter by 1
    tasks_completed += 1

    # Update the counter display text
    count_display.configure(text=f"Completed: {tasks_completed}")

    # Refresh both the active list and the completed list so the UI updates
    refresh_list()
    refresh_completed()


# This function adds whatever is in the entry box as a new task.
def show():
    # Get the text from the entry and strip leading/trailing whitespace
    item = input_entry.get().strip()

    # If the user typed nothing (or only spaces), show a warning and stop
    if not item:
        warning.configure(
            text="Please enter a task!",
            text_color="darkred"
        )
        return   # exit early — don't add an empty task

    # Add the task to the active list
    tasks.append(item)
    # Clear the warning message (in case it was showing)
    warning.configure(text="")
    # Clear the input box so the user can type the next task
    input_entry.delete(0, "end")
    # Refresh the active list so the new task appears
    refresh_list()


# Press Enter to add a task (same as clicking the button, but no button exists —
# the user just hits Enter inside the entry box)
input_entry.bind("<Return>", lambda event: show())

# Start the app's main event loop — keeps the window open and responsive
app.mainloop()
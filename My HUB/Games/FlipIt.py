# Import CustomTkinter for a modern, sleek GUI look
import customtkinter as ctk
# Import random to shuffle the game items before each match
import random
# Import messagebox from standard tkinter to display native victory/alert popups
from tkinter import messagebox

# =====================================================================
# INITIAL APPLICATION SETUP & WINDOW CONFIGURATION
# =====================================================================

# Initialize the main CustomTkinter application window context
root = ctk.CTk()

# Set the window title that displays in the OS top title bar
root.title("FlipIt")

ctk.set_appearance_mode("dark") # Makes the application dark themed

# Set the window dimensions (550px width, 700px height) and lock its 
# initial boot position to the absolute top-left corner of the screen (+0+0)
root.geometry("550x700+0+0")  

# Grid Column Configure: Give columns 0 through 5 an equal layout "weight" of 1.
# This forces CustomTkinter to distribute window width completely evenly 
# across all 6 horizontal columns, allowing the cards to stretch cleanly.
root.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

# Grid Row Configure: Give rows 0 through 6 an equal layout "weight" of 1.
# This distributes window height perfectly across all 7 vertical rows.
# Row 0 handles the game Title. Rows 1 to 6 handle the 32 card slots.
root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)


# =====================================================================
# UI TITLE COMPONENT
# =====================================================================

# Create the visual header label with large italicized and bold styling
title = ctk.CTkLabel(root, text="FlipIt", font=("Helvetica", 40, "italic", "bold"))

# Place the title securely in Row 0. 
# 'columnspan=6' stretches the label spanning across all 6 columns so it centers perfectly.
# 'pady=15' adds spacing above/below, and 'sticky="nsew"' expands it to fill its slot.
title.grid(row=0, column=0, columnspan=6, pady=15, sticky="nsew")


# =====================================================================
# GLOBAL GAME STATE VARIABLES
# =====================================================================

# Our master list of 32 total cards (16 unique pairs of matching emojis)
symbols = [
    "💩", "💩", "😂", "😂", "✔️", "✔️", "❌", "❌", 
    "🚀", "🚀", "🤑", "🤑", "💔", "💔", "👍", "👍", 
    "🤩", "🤩", "🤯", "🤯", "😡", "😡", "🦈", "🦈", 
    "🪰", "🪰", "🥶", "🥶", "😭", "😭", "👽", "👽"
]

# Tracks the first card button clicked during a player's turn. 
# Initialized to None because no turn has started yet.
first_card = None

# Keeps count of successfully matched pairs. 
# The game ends when this counter hits 16 (half the length of symbols).
matched_pairs = 0


# =====================================================================
# CORE GAME PLAY LOGIC
# =====================================================================

def show_card(btn, symbol):
    """
    Triggered every single time a player clicks any card button on the grid.
    Handles turning cards over, comparing matches, freezing wins, and clearing fails.
    """
    # Bring in global variables so we can modify game state across clicks
    global first_card, matched_pairs
    
    # SAFETY GUARD: If the button clicked is NOT a "?", it means it's already flipped 
    # face-up or disabled. Exit the function early to prevent double-click bugs!
    if btn.cget("text") != "?":
        return
        
    # Reveal the underlying emoji assigned to this specific button
    btn.configure(text=symbol)
    
    # PHASE 1: Checking if this is the very FIRST card turned over this turn
    if first_card is None:
        # Save this button object into memory so we can compare it to the next click
        first_card = btn
        
    # PHASE 2: This is the SECOND card turned over this turn. Time to compare!
    else:
        # Force the UI to refresh instantly so the player can actually see the 
        # second symbol render on screen before the engine pauses
        root.update()
        
        # Pause the application for 500 milliseconds (half a second) 
        # so the player has time to look at the cards and memorize them
        root.after(500)
        
        # CONDITION A: The two cards MATCH! (Their text values match)
        if first_card.cget("text") == btn.cget("text"):
            # Turn both buttons unclickable so they can't be modified again
            first_card.configure(state="disabled", fg_color="#2ecc71")
            btn.configure(state="disabled", fg_color="#2ecc71")
            
            # Increment our match tracking scoreboard counter
            matched_pairs += 1
            
            # WIN CONDITION: Have we found all 16 matching pairs?
            if matched_pairs == len(symbols) // 2:
                # Trigger a victory popup message box to celebrate
                messagebox.showinfo("Victory!", "You matched all pairs! 🎉")
                # Wipe the board clear and spin up a fresh round automatically
                clear_board()
                
        # CONDITION B: The two cards DO NOT MATCH!
        else:
            # Hide the emojis by restoring their text values back to generic question marks
            first_card.configure(text="?")
            btn.configure(text="?")
            
        # RESET STEP: Turn is officially over. Reset our first_card variable 
        # back to None so the player can start a brand new pair attempt.
        first_card = None


# =====================================================================
# GRID GENERATION AND BOARD MANAGEMENT
# =====================================================================

def make_board():
    """
    Shuffles game pieces, resets states, calculates a math-based matrix layout, 
    and instantiates 32 unique CustomTkinter button widgets.
    """
    global symbols, first_card, matched_pairs
    
    # Hard-reset game tracking values so code execution behaves perfectly on restart
    first_card = None
    matched_pairs = 0
    
    # Scramble the emoji positions randomly so every single playthrough layout is unique
    random.shuffle(symbols)
    
    # Loop over all 32 elements using enumerate to track index position and the emoji value
    for index, symbol in enumerate(symbols):
        
        # GRID LAYOUT GENERATION MATH:
        # Floor division '// 6' converts indices 0-31 into rows 0 to 5.
        # Adding '+ 1' shifts the entire grid down 1 row, leaving Row 0 completely free for the Title.
        row = (index // 6) + 1  
        
        # Modulo '% 6' converts indices 0-31 into repeating column loops of 0, 1, 2, 3, 4, 5.
        col = index % 6
        
        # Create a stylized card button instance inside the window
        card = ctk.CTkButton(
            root, 
            text="?",                   # Start face-down as a mystery question mark
            font=("Arial", 20),         # Use a clear, large font size for emojis
            width=50,                   # Base pixel constraints to keep layout compact
            height=70,
            text_color="black", 
            hover_color="lightgrey", 
            fg_color="white",
        )
        
        # LAMBDA ARGUMENT LOCKING MECHANISM:
        # We assign explicit defaults: 'btn=card' captures this specific iteration's button, 
        # and 'symbol=symbol' locks down its current matching emoji string.
        # This prevents Python from accidentally assigning the last looped value to all buttons!
        card.configure(command=lambda btn=card, symbol=symbol: show_card(btn, symbol))
        
        # Mount the card into the UI using our dynamically calculated grid row and column coordinates
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")


def clear_board():
    """
    Safely tears down matching grid buttons to prepare for a game reset 
    without accidentally deleting the top text title.
    """
    # Iterate through every single UI widget sitting inside the application window
    for widget in root.winfo_children():
        # CRITICAL FILTER: Only target and destroy CTkButton instances.
        # This leaves our CTkLabel (the Title) completely untouched!
        if isinstance(widget, ctk.CTkButton):
            widget.destroy()
        
    # Re-run the board generator loop to populate a freshly randomized card deck grid
    make_board()


# =====================================================================
# GAME RUNTIME EXECUTION
# =====================================================================

# Execute our board creation routine to generate the game layout on boot
make_board()

# Start the continuous, infinite application event processing loop. 
# This keeps the window open, listening for clicks and rendering visuals.
root.mainloop()

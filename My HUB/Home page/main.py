import customtkinter as ctk
import requests
import subprocess
import sys
import os


# ---------------- GAME LINKS ----------------

def htb():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "Hit The Button.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])


def cps():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "CPS Tester.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])


def typing():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "Typing Tester.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])


def reactiontest():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "Reaction Time Tester.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])


def calculator():
    calc_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "Calculator.py"
        )
    )
    subprocess.Popen([sys.executable, calc_path])

def flipit():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "FlipIt.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])
    
def todo():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "TaskForge.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])
    
def study_timer():
    games_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "Games",
            "LockIn",
            "LockIn.py"
        )
    )
    subprocess.Popen([sys.executable, games_path])
    
# ---------------- API ----------------

geo = "https://geocoding-api.open-meteo.com/v1/search"
url = "https://api.open-meteo.com/v1/forecast"


# ---------------- MAIN WINDOW ----------------

main = ctk.CTk()

main.title("EMPEROR HUB")

size = f"{main.winfo_screenwidth()}x{main.winfo_screenheight()}+0+0"
main.geometry(size)

ctk.set_appearance_mode("dark")

# GRID: 3 columns (weather | middle | games) and 3 rows (title | description | content)
main.grid_columnconfigure(0, weight=0, minsize=400)
main.grid_columnconfigure(1, weight=1)
main.grid_columnconfigure(2, weight=0, minsize=350)
main.grid_rowconfigure(0, weight=0)
main.grid_rowconfigure(1, weight=0)
main.grid_rowconfigure(2, weight=1)


# ---------------- DARK MODE ----------------

def change_mode():
    if switch.get() == 1:
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")


# ---------------- WEATHER ----------------

def search():
    city = city_get.get()
    WEATHER_CODES = {
        0: "Clear sky",                                            # totally clear
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",      # cloud cover levels
        45: "Fog", 48: "Depositing rime fog",                      # foggy conditions
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",  # drizzle levels
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",         # freezing drizzle
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",           # rain levels
        66: "Light freezing rain", 67: "Heavy freezing rain",               # freezing rain
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",  # snow levels
        77: "Snow grains",                                         # tiny snow grains
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",  # showers
        85: "Slight snow showers", 86: "Heavy snow showers",       # snow showers
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",  # storms
    }
    try:
        geo_params = {"name": city}

        geodata = requests.get(
            geo,
            params=geo_params,
            timeout=5
        ).json()

        latitude = geodata["results"][0]["latitude"]
        longitude = geodata["results"][0]["longitude"]

        coords = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code,apparent_temperature"
        }

        response = requests.get(
            url,
            params=coords,
            timeout=5
        )

        data = response.json()

        current_data = data["current"]

        temp = current_data["temperature_2m"]
        wind = current_data["wind_speed_10m"]
        code = current_data["weather_code"]

        temp_label.configure(
            text=f"Temperature: {temp}°C🌡️"
        )

        wind_label.configure(
            text=f"Wind: {wind} km/h💨"
        )
        
        humidity = current_data["relative_humidity_2m"]
        apparent_temp = current_data["apparent_temperature"]
        
        humidity_label.configure(
            text=f"Humidity: {humidity}%💧"
        )
        
        apparent_temp_label.configure(
            text=f"Feels like: {apparent_temp}°C🌡️"
        )
    
        weather_code.configure(
        text=f"Weather Type: {WEATHER_CODES.get(code, 'Unknown')}",
        wraplength=200
        )

       


    except (KeyError, IndexError, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        temp_label.configure(text="City not found or connection error",wraplength=200)
        wind_label.configure(text="-")
        humidity_label.configure(text="-")
        apparent_temp_label.configure(text="-")
        weather_code.configure(text="-")


# ---------------- HOME ----------------

label = ctk.CTkLabel(
    main,
    text="THE EMPERORS HUB",
    font=("Arial", 85)
)

label.grid(row=0, column=1)


explanation = ctk.CTkLabel(
    main,
    text="Welcome to the Emperors Hub!\nNeed to play fun games or utilities but arent allowed phones or websites are banned in school or work?\nUse the Emperors Hub!",
    font=("Arial", 20),
    wraplength=950
)

explanation.grid(row=1, column=1)


# ---------------- WEATHER FRAME ----------------

weather_frame = ctk.CTkFrame(
    main,
    width=400,
    border_width=2
)

weather_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

weather_frame.grid_columnconfigure(0, weight=1)
weather_frame.grid_rowconfigure(9, weight=1)   


weather_title = ctk.CTkLabel(
    weather_frame,
    text="WEATHER",
    font=("Arial", 35)
)

weather_title.grid(row=0, column=0, pady=40)


city_get = ctk.CTkEntry(
    weather_frame,
    placeholder_text="Enter city",
    width=280,
    height=45
)

city_get.grid(row=1, column=0, pady=10)


search_button = ctk.CTkButton(
    weather_frame,
    text="Search",
    command=search,
    width=200,
    height=45,
    fg_color="white",
    hover_color="lightgray",
    text_color="black"
)

search_button.grid(row=2, column=0, pady=15)


temp_label = ctk.CTkLabel(
    weather_frame,
    text="Temperature: --°C",
    font=("Arial", 25)
)

temp_label.grid(row=3, column=0, pady=30)


wind_label = ctk.CTkLabel(
    weather_frame,
    text="Wind: -- km/h",
    font=("Arial", 25)
)

wind_label.grid(row=4, column=0, pady=10)

humidity_label = ctk.CTkLabel(
    weather_frame,
    text="Humidity: --%",
    font=("Arial", 25)
)

humidity_label.grid(row=5, column=0, pady=10)

apparent_temp_label = ctk.CTkLabel(
    weather_frame,
    text="Feels like: --°C",
    font=("Arial", 25)
)

apparent_temp_label.grid(row=6, column=0, pady=10)

weather_code = ctk.CTkLabel(
    weather_frame,
    text="Weather Type:",
    font=("Arial", 25)
)

weather_code.grid(row=8, column=0, pady=10)

switch = ctk.CTkSwitch(
    weather_frame,
    text="Light Mode",
    command=change_mode,
    switch_width=100,
    switch_height=40,
    font=("Arial", 15)
)

switch.grid(row=9, column=0, pady=(10), sticky="n")


# ---------------- GAMES FRAME ----------------

game_frame = ctk.CTkFrame(
    main,
    width=350,
    border_width=2
)

game_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")

game_frame.grid_columnconfigure(0, weight=1)


games_title = ctk.CTkLabel(
    game_frame,
    text="GAMES",
    font=("Arial", 35),
)

games_title.grid(row=0, column=0, pady=40)


# ---------------- GAME BUTTONS ----------------

htb_button = ctk.CTkButton(
    game_frame,
    text="HIT THE BUTTON",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    command=htb,
    width=220,
    height=45
)

htb_button.grid(row=1, column=0, pady=5)


cps_button = ctk.CTkButton(
    game_frame,
    text="CPS TESTER",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    command=cps,
    width=220,
    height=45
)

cps_button.grid(row=2, column=0, pady=5)


typing_button = ctk.CTkButton(
    game_frame,
    text="TYPING TESTER",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    command=typing,
    width=220,
    height=45
)

typing_button.grid(row=3, column=0, pady=5)


reactiontest_button = ctk.CTkButton(
    game_frame,
    text="REACTION TESTER",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    command=reactiontest,
    width=220,
    height=45
)

reactiontest_button.grid(row=4, column=0, pady=5)

flipit_button = ctk.CTkButton(
    game_frame,
    text="FLIP IT",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    command=flipit,
    width=220,
    height=45
)

flipit_button.grid(row=5, column=0, pady=5)


# ---------------- UTILITIES (middle) ----------------

utility_frame = ctk.CTkFrame(main, fg_color="transparent")
utility_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)

utility_frame.grid_columnconfigure(0, weight=1, uniform="utility_col")
utility_frame.grid_columnconfigure(1, weight=1, uniform="utility_col")
utility_frame.grid_rowconfigure(0, weight=1, uniform="utility_row")
utility_frame.grid_rowconfigure(1, weight=1, uniform="utility_row")
utility_frame.grid_rowconfigure(2, weight=1, uniform="utility_row")

# 6 slots in a 2 x 3 grid. Slot 1 holds the calculator, slots 2-6 are EMPTY for future utilities
slot_1 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

slot_2 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

slot_3 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

slot_4 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

slot_5 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_5.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

slot_6 = ctk.CTkFrame(utility_frame, fg_color="transparent", border_width=2, corner_radius=20)
slot_6.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Centre the calculator button inside slot 1
slot_1.grid_rowconfigure(0, weight=1)
slot_1.grid_columnconfigure(0, weight=1)

slot_2.grid_rowconfigure(0, weight=1)
slot_2.grid_columnconfigure(0, weight=1)

slot_3.grid_rowconfigure(0, weight=1)
slot_3.grid_columnconfigure(0, weight=1)

slot_4.grid_rowconfigure(0, weight=1)
slot_4.grid_columnconfigure(0, weight=1)

slot_5.grid_rowconfigure(0, weight=1)
slot_5.grid_columnconfigure(0, weight=1)

slot_6.grid_rowconfigure(0, weight=1)
slot_6.grid_columnconfigure(0, weight=1)


# ---------------- Utilities ----------------

calculator_button = ctk.CTkButton(
    slot_1,
    text="Calculator",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    font=("Arial", 20),
    width=300,
    height=55,
    command=calculator
)

calculator_button.grid(row=0, column=0, padx=20, pady=20)

todo_button = ctk.CTkButton(
    slot_2,
    text="To Do App",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    font=("Arial", 20),
    width=300,
    height=55,
    command=todo
)

todo_button.grid(row=0, column=0, padx=20, pady=20)

study_timer_button = ctk.CTkButton(
    slot_3,
    text="Study Timer",
    fg_color="white",
    hover_color="lightgray",
    text_color="black",
    font=("Arial", 20),
    width=300,
    height=55,
    command=study_timer
)

study_timer_button.grid(row=0, column=0, padx=20, pady=20)

temp_label1 = ctk.CTkLabel(slot_4, text="New Utilities Coming soon!", font=("Arial", 20))
temp_label1.grid(row=0, column=0, padx=20, pady=20)

temp_label2 = ctk.CTkLabel(slot_5, text="New Utilities Coming soon!", font=("Arial", 20))
temp_label2.grid(row=0, column=0, padx=20, pady=20)

temp_label3 = ctk.CTkLabel(slot_6, text="New Utilities Coming soon!", font=("Arial", 20))
temp_label3.grid(row=0, column=0, padx=20, pady=20)
# ---------------- RUN ----------------

main.mainloop()

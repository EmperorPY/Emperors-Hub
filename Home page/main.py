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
    

# ---------------- API ----------------

geo = "https://geocoding-api.open-meteo.com/v1/search"
url = "https://api.open-meteo.com/v1/forecast"


# ---------------- MAIN WINDOW ----------------

main = ctk.CTk()

main.title("EMPEROR HUB")

size = f"{main.winfo_screenwidth()}x{main.winfo_screenheight()}+0+0"
main.geometry(size)

ctk.set_appearance_mode("dark")


# ---------------- DARK MODE ----------------

def change_mode():
    if switch.get() == 1:
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")


# ---------------- WEATHER ----------------

def search():
    city = city_get.get()

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
            "current": "temperature_2m,wind_speed_10m"
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

        temp_label.configure(
            text=f"Temperature: {temp}°C🌡️"
        )

        wind_label.configure(
            text=f"Wind: {wind} km/h💨"
        )

    except (KeyError, IndexError):
        temp_label.configure(text="City not found")
        wind_label.configure(text="")


# ---------------- HOME ----------------

label = ctk.CTkLabel(
    main,
    text="THE EMPERORS HUB",
    font=("Arial", 85),
    text_color="orange"
)

label.pack()


explanation = ctk.CTkLabel(
    main,
    text="Welcome to the Emperors Hub!\nNeed to check weather or play undwinding games but arent allowed phones or websites are banned?\nUse the Emperors Hub!",
    font=("Arial", 20),
    text_color="white"
)

explanation.pack()


# ---------------- WEATHER FRAME ----------------

weather_frame = ctk.CTkFrame(
    main,
    width=400,
    border_width=2
)

weather_frame.place(
    x=0,
    y=0,
    relheight=1
)


weather_title = ctk.CTkLabel(
    weather_frame,
    text="WEATHER",
    font=("Arial", 35),
    text_color="orange"
)

weather_title.pack(pady=40)


city_get = ctk.CTkEntry(
    weather_frame,
    placeholder_text="Enter city",
    width=280,
    height=45
)

city_get.pack(pady=10)


search_button = ctk.CTkButton(
    weather_frame,
    text="Search",
    command=search,
    width=200,
    height=45,
    fg_color="orange",
    text_color="black"
)

search_button.pack(pady=15)


temp_label = ctk.CTkLabel(
    weather_frame,
    text="Temperature: --°C",
    font=("Arial", 25)
)

temp_label.pack(pady=30)


wind_label = ctk.CTkLabel(
    weather_frame,
    text="Wind: -- km/h",
    font=("Arial", 25)
)

wind_label.pack(pady=10)


switch = ctk.CTkSwitch(
    weather_frame,
    text="TEACHER FLASHBANG",
    command=change_mode,
    switch_width=100,
    switch_height=40,
    font=("Arial", 15)
)

switch.pack(pady=10)


# ---------------- GAMES FRAME ----------------

game_frame = ctk.CTkFrame(
    main,
    width=350,
    border_width=2
)

game_frame.place(
    relx=1.0,
    rely=0,
    anchor="ne",
    relheight=1
)


games_title = ctk.CTkLabel(
    game_frame,
    text="GAMES",
    font=("Arial", 35),
    text_color="orange"
)

games_title.pack(pady=40)


# ---------------- GAME BUTTONS ----------------

htb_button = ctk.CTkButton(
    game_frame,
    text="HIT THE BUTTON",
    fg_color="orange",
    text_color="black",
    command=htb,
    width=220,
    height=45
)

htb_button.pack(pady=5)


cps_button = ctk.CTkButton(
    game_frame,
    text="CPS TESTER",
    fg_color="orange",
    text_color="black",
    command=cps,
    width=220,
    height=45
)

cps_button.pack(pady=5)


typing_button = ctk.CTkButton(
    game_frame,
    text="TYPING TESTER",
    fg_color="orange",
    text_color="black",
    command=typing,
    width=220,
    height=45
)

typing_button.pack(pady=5)


reactiontest_button = ctk.CTkButton(
    game_frame,
    text="REACTION TESTER",
    fg_color="orange",
    text_color="black",
    command=reactiontest,
    width=220,
    height=45
)

reactiontest_button.pack(pady=5)


# ---------------- EMERGENCY CALCULATOR ----------------

calculator_button = ctk.CTkButton(
    main,
    text="EMERGENCY CALCULATOR",
    fg_color="orange",
    text_color="black",
    font=("Arial", 20),
    width=300,
    height=55,
    command=calculator
)

calculator_button.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ---------------- RUN ----------------

main.mainloop()
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import threading
import tkinter as tk
from tkinter import scrolledtext

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()
API_KEY = "d027fa66180cce7b01e67717ba54ac32"
listening = False

# Speak function
def speak(text):
    log(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Log to GUI
def log(message):
    output.insert(tk.END, message + "\n")
    output.see(tk.END)

# Listen function
def listen():
    global listening
    with sr.Microphone() as source:
        log("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            log(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")
    return ""

# Weather info
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {desc}.")
    else:
        speak("I couldn't get the weather information.")

# Handle commands
def handle_command(command):
    if "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time}")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "your name" in command:
        speak("I am your Python assistant.")
    elif "weather" in command:
        speak("Which city do you want the weather for?")
        city = listen()
        if city:
            get_weather(city)
    elif "stop" in command or "shutdown" in command:
        speak("Goodbye!")
        stop_listening()
        root.quit()
    else:
        speak("I can’t do that yet.")

# Voice assistant main loop
def assistant_loop():
    global listening
    speak("Hello! How can I help you?")
    listening = True
    while listening:
        command = listen()
        if command:
            handle_command(command)

def start_listening():
    thread = threading.Thread(target=assistant_loop)
    thread.daemon = True
    thread.start()

def stop_listening():
    global listening
    listening = False
    log("Stopped Listening.")

# GUI setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x400")

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
output.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

start_btn = tk.Button(btn_frame, text="Start Listening", command=start_listening)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(btn_frame, text="Stop", command=stop_listening)
stop_btn.grid(row=0, column=1, padx=10)

exit_btn = tk.Button(btn_frame, text="Exit", command=root.quit)
exit_btn.grid(row=0, column=2, padx=10)

root.mainloop()

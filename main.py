import pyttsx3
import speech_recognition as sr
import datetime
import os
import paho.mqtt as mqtt
import smtplib
import wikipedia
import webbrowser

engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(audio):
    engine.say(audio)
    engine.runAndWait()


def welcome():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good Morning!")
    elif hour >= 12 and hour < 16:
        talk("Good Afternoon!")
    elif hour >= 16 and hour < 19:
        talk("Good Evening!")
    talk("Welcome Sir. How may I help you")


def inputVC():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Sorry sir I did't get that")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'password')
    server.sendmail('your email id', to, content)
    server.close()

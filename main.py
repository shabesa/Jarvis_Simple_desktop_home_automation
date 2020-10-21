import pyttsx3
import speech_recognition as sr
import datetime
import os
import paho.mqtt as mqtt
import smtplib
import wikipedia
import webbrowser
from time import sleep

music_dir = 'C:\\Users\\DELL\\Desktop\\shabesa\\Musiq\\Bigil-320kbps-MassTamilan.org'


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
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


def byebye():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk('happy day sir')
    elif hour >= 12 and hour < 16:
        talk('happy noon sir')
    elif hour >= 16 and hour < 20:
        talk('happy evening sir')
    else:
        talk('good night sir')
    talk('bye bye sir')


if __name__ == "__main__":
    talk('Hi I am Jarvis. Your personal assistant')
    welcome()
    while True:
        query = inputVC().lower()

        if 'play music' in query:
            songs = os.listdir(music_dir)
            print(songs)
            sleep(5)
            talk('sir song number please')
            songVal = inputVC()
            os.startfile(os.path.join(music_dir, songs[int(songVal)]))
        elif 'wait' in query:
            talk('sir duration')
            waitVal = inputVC()
            sleep(int(waitVal))
        elif 'send a mail' in query:
            try:
                talk("What should I say?")
                content = inputVC()
                talk("sir please enter the mail id")
                to = input()
                sendEmail(to, content)
                talk("Email has been sent!")
            except Exception as e:
                print(e)
                talk("Sorry sir. I am not able to send this email")
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            talk(f"Sir, the time is {strTime}")
        elif 'jarvis are you here' in query:
            talk('At your service sir')
        elif 'turn on light' in query:
            talk('Sir which room?')
            room = inputVC()
            if room == 'master bedroom':
                talk(f'turning on lights in {room}')
        elif 'surf' or 'browse' in query:
            webbrowser.open('google.co.in')       
        elif 'thank you' in query:
            talk('my pleasure sir')
        elif 'bye bye' in query:
            byebye()
            break

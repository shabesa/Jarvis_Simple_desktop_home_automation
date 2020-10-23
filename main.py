# importing the necessary modules
import pyttsx3
import speech_recognition as sr
import datetime
import os
import paho.mqtt as mqtt
import smtplib
import wikipedia
import webbrowser
from time import sleep
import vlc

# setting the state for media
songIsPlaying = False
videoIsPlaying = False

# adding media directories
# example_dir = 'C:\\Users\\DELL\\Desktop\\'
movie_dir = 'add your movie directory'
music_dir = 'add you song directory'

# init the vlc player
media_player = vlc.MediaPlayer()

# init the text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# making to speak the text
def talk(audio):
    engine.say(audio)
    engine.runAndWait()


# welcome when running program
def welcome():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good Morning!")
    elif hour >= 12 and hour < 16:
        talk("Good Afternoon!")
    elif hour >= 16 and hour < 19:
        talk("Good Evening!")
    talk("Welcome Sir. How may I help you")


# function to get voice input and recognizing
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


# function to start server to send mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'password')
    server.sendmail('your email id', to, content)
    server.close()


# function to stop the function
def byebye():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk('have a nice day sir')
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

        if 'drop my needle' or 'play music' in query:
            songs = os.listdir(music_dir)
            print(songs)
            sleep(5)
            talk('sir song number please')
            songVal = inputVC()
            stoplay = os.path.join(music_dir, songs[int(songVal)])
            sMedia = vlc.Media(stoplay)
            media_player.set_media(sMedia)
            media_player.play()
            songIsPlaying = True

        elif 'what is the song volume' in query:
            if songIsPlaying is True:
                csv = media_player.audio_get_volume()
                print(csv)
                talk(f"sir the volume is {csv} percent")
            else:
                talk('sir there is no media playing')

        elif 'set song volume' in query:
            if songIsPlaying is True:
                talk('sir what is the volume level that you want?')
                svVal = inputVC()
                media_player.audio_set_volume(int(svVal))
                talk(f'sir volume is set to {svVal} percent')
            else:
                talk('sir there is no media playing currently')

        elif 'hold song point' in query:
            media_player.pause()
            talk('song paused')
            songIsPlaying = False

        elif 'continue song' in query:
            media_player.play()

        elif 'stop song' in query:
            media_player.stop()
            songIsPlaying = False

        elif 'play video' in query:
            movies = os.listdir(movie_dir)
            print(movies)
            sleep(5)
            talk('sir video number please')
            movieVal = inputVC()
            mtoPlay = os.path.join(movie_dir, movies[int(movieVal)])
            mMedia = vlc.Media(mtoPlay)
            media_player.set_media(mMedia)
            media_player.play()
            videoIsPlaying = True

        elif 'what is the video volume' in query:
            if videoIsPlaying is True:
                cmv = media_player.audio_get_volume()
                print(cmv)
                talk(f"sir the volume is{cmv} percent")
            else:
                talk('sir there is no media playing')

        elif 'set video volume' in query:
            if videoIsPlaying is True:
                talk('sir what is the volume level that you want?')
                mvVal = inputVC()
                media_player.audio_set_volume(int(mvVal))
                talk(f'sir volume is set to {mvVal} percent')
            else:
                talk('sir there is no video playing currently')

        elif 'hold scene' in query:
            media_player.pause()
            talk('video paused')
            videoIsPlaying = False

        elif 'continue video' in query:
            media_player.play()

        elif 'stop video' in query:
            media_player.stop()
            videoIsPlaying = False

        elif 'wait' in query:
            talk('sir duration')
            waitVal = inputVC()
            sleep(int(waitVal))

        elif 'send a mail' in query:
            try:
                talk("What should I say?")
                content = inputVC()
                talk("sir please enter the mail id")
                to = input('mail id: ')
                sendEmail(to, content)
                talk("Email has been sent!")
            except Exception as e:
                print(e)
                talk("Sorry sir. I am not able to send this email")

        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            talk(f"Sir, the time is {strTime}")

        elif 'jarvis' in query:
            talk('At your service sir')

        elif 'turn on light' in query:
            talk('Sir which room?')
            room = inputVC()
            if room == 'master bedroom':
                talk(f'turning on lights in {room}')

        elif 'thank you' in query:
            talk('my pleasure sir')

        elif 'bye bye' in query:
            byebye()
            break

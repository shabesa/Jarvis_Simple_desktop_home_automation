# importing the necessary modules
import pyttsx3
import speech_recognition as sr
import datetime
import os
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import serial
import smtplib
import wikipedia
import webbrowser
from time import sleep
import vlc
from recog import facePass

faceis = False
userPin = [1, 2, 3]

# setting the state for media
songIsPlaying = False
videoIsPlaying = False

# adding media directories
# example_dir = 'C:\\Users\\%user name%\\Desktop\\'
movie_dir = 'add your movie directory'
music_dir = 'add your music directory'

# init the vlc player
media_player = vlc.MediaPlayer()

# mqtt host
host = "enter your ip address"
mqtt_alive = False

# init the text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# setting serial comms
# board = serial.Serial(COM6, 9600)


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
    talk("Welcome Sir.")


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


# function to start the server to send mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'password')
    server.sendmail('your email id', to, content)
    server.close()


# function to stop the code
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
    talk('see you later sir')


# functions to  check the status of mqtt server
def mqtt_ping(ping):
    talk("checking mqtt server")
    try:
        publish.single("ping", payload="mqtt", hostname=host)
        test = subscribe.simple("pingOut", hostname=host)
        print('%s' % (test.payload.decode('ascii')))
        if test.payload.decode('ascii') == "mqtt":
            talk("mqtt server up and running")
            ping = True
    except Exception as e:
        print(e)
        talk("sir mqtt server is not responding")
        ping = False
    return ping


def systemCheck(start):
    talk("sir i am initiating systems check")
    if start is True:
        publish.single("check", payload="check", hostname=host)
        system1 = subscribe.simple("status", hostname=host)
        print('%s' % (system1.payload.decode('ascii')))
        if system1.payload.decode('ascii') == "board 1 online":
            talk("sir board 1 is online")
        else:
            talk("sir the systems are offline")
    else:
        talk("systems check failed as the mqtt server is down")


def room_temp():
    if mqtt_alive is True:
        talk("fetching room temperature data")
        publish.single("temp", payload="temp", hostname=host)
        temperature = subscribe.simple("tdata", hostname=host)
        print("%s" % (temperature.payload.decode('ascii')))
        talk(temperature.payload.decode('ascii') + "degree celcius")
    else:
        talk("mqtt failure sir, cannot fetch the data")


if __name__ == "__main__":
    talk('Hi I am Jarvis. Your personal assistant')
    talk('scanning face for authorization')
    faceis = facePass(faceis)
    if faceis == "Shabesa":
        talk("face verified")
        talk("sir enter your pin for second step authorization")
        pin = int(input('enter your pin: '))
        if pin in userPin:
            talk("Authorization complete. booting system")
            welcome()
            mqtt_alive = mqtt_ping(mqtt_alive)
            systemCheck(mqtt_alive)
            talk("sir start up check is complete")
            while True:
                query = inputVC().lower()

                if 'play music' in query:
                    songs = list(os.listdir(music_dir))
                    n = 0
                    for i in songs:
                        print(n, '.', i)
                        n += 1
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
                    if waitVal == 'media time' or waitVal == 'time':
                        dur = media_player.get_length()
                        print((dur / 1000) / 60)
                        sleep(dur / 1000)
                    else:
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

                elif 'what is the room temperature' in query:
                    room_temp()

                elif 'jarvis' in query:
                    talk('At your service sir')

                elif 'what are you doing' in query:
                    talk('waiting for your command sir')

                elif 'initiate systems check' in query:
                    systemCheck(mqtt_alive)

                elif 'turn on lights' in query:
                    if mqtt_alive is True:
                        talk('Sir which room?')
                        room = inputVC()
                        if room == 'master bedroom':
                            talk(f'turning on lights in {room}')
                            publish.single("lightsOut", payload="mblon", hostname=host)
                        elif room == 'server room':
                            talk(f'turning on lights in {room}')
                            publish.single("lightsOut", payload="srlon", hostname=host)
                    elif mqtt_alive is False:
                        talk("sorry sir mqtt server is down")

                elif 'turn off lights' in query:
                    if mqtt_alive is True:
                        talk('Sir which room?')
                        room = inputVC()
                        if room == 'master bedroom':
                            talk(f'turning off lights in {room}')
                            publish.single("lightsOut", payload="mblof", hostname=host)
                        elif room == 'server room':
                            talk(f'turning off lights in {room}')
                            publish.single("lightsOut", payload="srlof", hostname=host)
                    elif mqtt_alive is False:
                        talk("sorry sir mqtt server is down")

                elif 'ok' in query:
                    talk("fine sir")

                elif 'thank you' in query:
                    talk('my pleasure sir')

                elif 'restart' in query:
                    talk("sir are you sure to restart?")
                    result = inputVC()
                    if result == "yes":
                        os.system('python "add your code directory"')
                        break

                elif 'bye bye' in query:
                    byebye()
                    break
    elif faceis == "Unknown":
        talk("I don't know you")
        talk("I am shut-ing down")


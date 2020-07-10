import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
import pywhatkit as kit
from gtts import gTTS
from time import ctime
from phue import Bridge
from ip_address import bridge_ip_address


r = sr.Recognizer()

def access_lights(bridge_ip_address):
    b = Bridge(bridge_ip_address)
    light_names_list = b.get_light_objects('name')
    return light_names_list

def film_lights_on():
        lights = access_lights(bridge_ip_address)
        for light in lights:
            lights[light].on = True
            lights[light].hue = 14000
            lights[light].saturation = 120


def film_lights_off():
    lights = access_lights(bridge_ip_address)
    for light in lights:
        lights[light].on = False
        lights[light].hue = 14000
        lights[light].saturation = 120

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            alexis_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
                alexis_speak('Sorry, I did not get that')
        except sr.RequestError:
                alexis_speak('Sorry, my speech service is down')
        return voice_data

def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if 'what is your name' in voice_data:
        alexis_speak('My name is Alexis')
    if 'what time is it' in voice_data:
        alexis_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speak('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speak('Here is the location of ' + location)
    if 'find music' in voice_data:
        find = record_audio('What to search on youtube?')
        url = 'https://www.youtube.com/results?search_query=' + find
        webbrowser.get().open(url)
        alexis_speak('Here is ' + find)
    if 'play' in voice_data:
        play = record_audio('What to play on youtube?')
        kit.playonyt(play)
        alexis_speak('Enjoy it :)')
        time.sleep(300)
    if 'wiki' in voice_data:
        wiki = record_audio('What do you want to search on Wikipedia?')
        url = 'https://en.wikipedia.org/wiki/' + wiki
        webbrowser.get().open(url)
        alexis_speak('Here is what i found on wikipedia about ' + wiki)
        time.sleep(60)
    if 'open' in voice_data:
        rec = record_audio('What to open?')
        if rec == 'calculator':
            os.system('calc')

#Light controll

    if 'turn on the light' in voice_data:
        film_lights_on()
    if 'turn off the light' in voice_data:
        film_lights_off()

    if 'exit' in voice_data:
        alexis_speak('Ok')
        exit()

time.sleep(1)
alexis_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)
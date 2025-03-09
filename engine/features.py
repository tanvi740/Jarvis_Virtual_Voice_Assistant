import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from hugchat import hugchat
import pyautogui as autogui
from playsound import playsound

import eel
import pvporcupine
import pyaudio
import pywhatkit as kit

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playassistantsound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)

OPENING_MESSAGE = "Opening "
def opencommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak(OPENING_MESSAGE+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak(OPENING_MESSAGE +query)
                    webbrowser.open(results[0][0])

                else:
                    speak(OPENING_MESSAGE +query)
                    try:
                        os.system(f'start {query}')  
                    except OSError:
                        speak("Application not found")
        except Exception as e:
            speak(f"Something went wrong: {str(e)}")
            

import pyautogui
import time



def playyoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(f"An error:{str(e)}")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
            
# find contacts
def findcontact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    
    except Exception:  # Or specify the exact exception
     speak('not exist in contacts')
     return 0, 0

def whatsapp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 9
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 13
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')

    for _ in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(jarvis_message)


# chat bot 
def chatbot(query):
    user_input = query.lower()
    chatbott = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    idd = chatbott.new_conversation()
    chatbott.change_conversation(idd)
    response =  chatbott.chat(user_input)
    print(response)
    speak(response)
    return response


def makecall(name, mobileno):
    mobileno =mobileno.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileno
    os.system(command)


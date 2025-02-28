import os
import re
import sqlite3
import webbrowser

from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
#playing the assistant sound function
import pywhatkit as kit

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
                speak (OPENING_MESSAGE+query)
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
            

       
         

def playyoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None    
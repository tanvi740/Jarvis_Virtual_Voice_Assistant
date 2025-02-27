import time
import pyttsx3
import eel
import speech_recognition as sr

def speak(text):
    
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    print(voices)
    engine.say(text)
    #eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        speak(query)
        eel.ShowHood() 
        eel.DisplayMessage(query)
        #time.sleep(2)
       
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
    return query.lower()



import pyttsx3
import speech_recognition as sr
import eel
import time





def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


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
        eel.DisplayMessage(query)
        time.sleep(2)
        
        
       
       
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    
    return query.lower()

SEND_MESSAGE = "send message"
PHONE_CALL = "phone call"
VIDEO_CALL="video call"

@eel.expose
def allcommands(message=1):

    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message    
        eel.senderText(query)

    try:
        
        if "open" in query:
            from engine.features import opencommand
            opencommand(query)
        elif "on youtube" in query:
            from engine.features import playyoutube
            playyoutube(query)
        
        elif SEND_MESSAGE in query or PHONE_CALL in query or VIDEO_CALL in query:
            from engine.features import findcontact, whatsapp,makecall
            contact_no,name=findcontact(query)
            if(contact_no!=0):
                speak("Which mode you want to use Whatspp or mobile")
                preference=takecommand()
                print(preference)
                
                if "mobile" in preference:
                    if SEND_MESSAGE  in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                       # sendmessage(message, contact_no, name)
                    elif PHONE_CALL in query:
                        makecall(name, contact_no)
                    else:
                        speak("please try again")

                elif "whatsapp" in preference:
                    message = ""
                    if SEND_MESSAGE  in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()        

            

                elif PHONE_CALL in query:
                   message='call'
                else:
                    message=VIDEO_CALL

                

                whatsapp(contact_no,query,message,name)

        else:
            from engine.features import chatbot
            chatbot(query)
    except Exception as e:
        print(f"Error:{str(e)}")                            
    
    eel.ShowHood()
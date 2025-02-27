from playsound import playsound
import eel
#playing the assistant sound function

@eel.expose
def playassistantsound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)
   
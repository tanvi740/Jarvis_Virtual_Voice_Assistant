import os
import subprocess
import eel

from engine.features import playassistantsound
from engine.command import takecommand
from engine.command import speak
from engine.auth import recoganize
def start():
  eel.init("www")
  playassistantsound()
  @eel.expose
  def init():
    subprocess.call(r'device.bat')
    eel.hideLoader()
    speak("Ready for Face Authentication")
    flag=recoganize.authenticateface()
    if flag==1:
      eel.hideFaceAuth()
      speak("Face Authentication Successful")
      eel.hideFaceAuthSuccess()
      speak("Welcome to the AI Assistant")
      eel.hideStart()
    else:
      speak("Face Authentication failed")  
 
  os.system('start msedge.exe --app="http://localhost:8000/index.html"')
  eel.start('index.html', mode=None, host='localhost', block=True)


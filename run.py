import keyboard
from main import start


def startjarvis():
    print("Jarvis is running...")
    start()

print("Press Windows+J to start Jarvis...")
keyboard.wait("win+j")  # जब तक Windows+J नहीं दबाते, रुकेगा
startjarvis()
import multiprocessing
import subprocess

# To run Jarvis
def startjarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# To run hotword
def listenhotword():
        # Code for process 2
        print("Process 2 is running.")
        from engine.features import hotword
        hotword()


    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startjarvis)
        p2 = multiprocessing.Process(target=listenhotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")
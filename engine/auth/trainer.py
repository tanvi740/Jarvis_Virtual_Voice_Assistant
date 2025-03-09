import cv2
import numpy as np
from PIL import Image #pillow package
import os

path = 'engine\\auth\\samples' # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
#Haar Cascade classifier is an effective object detection approach


def images_and_labels(path): # function to fetch the images and labels

    imagepaths = [os.path.join(path,f) for f in os.listdir(path)]     
    facesamples=[]
    ids = []

    for imagepath in imagepaths: # to iterate particular image path

        gray_img = Image.open(imagepath).convert('L') # convert it to grayscale
        img_arr = np.array(gray_img,'uint8') #creating an array

        person_id = int(os.path.split(imagepath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            facesamples.append(img_arr[y:y+h,x:x+w])
            ids.append(person_id )

    return facesamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = images_and_labels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('engine\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

print("Model trained, Now we can recognize your face.")
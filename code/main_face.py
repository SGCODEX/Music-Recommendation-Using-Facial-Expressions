#This is the raw code without using any fancy GUI or web tool
#Importing the libraries
import cv2
from keras.models import load_model
import numpy as np
import webbrowser
import requests
import re
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Function to play the first song from youtube queries
def play_first_song(final_emotion):
    search_query = f"https://www.youtube.com/results?search_query={final_emotion}+background+tunes"
    #webbrowser.open(search_query)
    #search_query = f"https://www.youtube.com/results?search_query=Hindi+sad+songs"
    response = requests.get(search_query)
    html_content = response.text
    match = re.search(r'/watch\?v=([^\"]+)', html_content)
    if match:
        video_id = match.group(1)
        #video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url = f"https://www.youtube.com/watch?v={video_id.encode('utf-8').decode('unicode_escape')}"
        webbrowser.open(video_url)
    
# Load the pre-trained facial expression recognition model
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5") 

# Define the list of emotions
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Create a cascade classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a connection to the camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Variable to store the final emotion
final_emotion = None

# Flag to indicate whether emotion capture has occurred
emotion_captured = False

# Flag for music part
Flag_final = False

# Callback function for mouse click
def on_button_click(event, x, y, flags, param):
    global final_emotion
    if event == cv2.EVENT_LBUTTONDOWN:
        final_emotion = emotion_label
        print("Final Emotion:", final_emotion)
        cap.release()
        cv2.destroyAllWindows()
        emotion_captured = True

# Create a named window
cv2.namedWindow('Facial Expression Recognition')

# Set the mouse callback function 
cv2.setMouseCallback('Facial Expression Recognition', on_button_click)


while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    #print("Read frame:", ret)

    # Check if the emotion has been captured
    if ret == False:
        play_first_song(final_emotion)
        break
        #print("breaking the loop")

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) which is the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (64, 64), interpolation=cv2.INTER_AREA)

        # Normalize the pixel values
        roi = roi_gray / 255.0

        # Reshape the image for the model
        roi = np.reshape(roi, (1, 64, 64, 1))

        # Make a prediction using the pre-trained model
        prediction = model.predict(roi)
        emotion_label = emotions[np.argmax(prediction)]

        # Draw a rectangle around the face and display the predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the button text
        button_text = "Capture Emotion"
        cv2.putText(frame, button_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


    # Display the frame
    cv2.imshow('Facial Expression Recognition', frame)
    #print("Display frame")

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #print("Key pressed")

# Release the camera and close all OpenCV windows
#print("About to release the camera and close windows")
cap.release()
cv2.destroyAllWindows()

#This is the code with PySimpleGUI as GUI for the project
#Importing the libraries
import cv2
import PySimpleGUI as sg
from keras.models import load_model
import numpy as np
import webbrowser
from threading import Thread
import requests
import re

# Load the pre-trained facial expression recognition model
model = load_model('code/model/fer2013_mini_XCEPTION.102-0.66.hdf5')
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def detect_emotion(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (64, 64), interpolation=cv2.INTER_AREA)
        roi = roi_gray / 255.0
        roi = np.reshape(roi, (1, 64, 64, 1))
        prediction = model.predict(roi)
        emotion_label = emotions[np.argmax(prediction)]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        return frame, emotion_label
    return None, None  # Return None when no faces are detected

def video_thread(window):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    current_emotion = None
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))  # Resize frame for better performance
            frame_with_faces, current_detected_emotion = detect_emotion(frame, face_cascade)
            if frame_with_faces is not None:
                imgbytes = cv2.imencode('.png', frame_with_faces)[1].tobytes()
                window['-IMAGE-'].update(data=imgbytes)
                if current_detected_emotion != current_emotion:
                    window['-EMOTION-'].update(value=f'Detected Emotion: {current_detected_emotion}')
                    current_emotion = current_detected_emotion

def play_song_with_emotion(emotion, window):
    search_query = f"https://www.youtube.com/results?search_query={emotion}+weekend+beats"
    response = requests.get(search_query)
    html_content = response.text
    match = re.search(r'/watch\?v=([^\"]+)', html_content)
    if match:
        video_id = match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(video_url)

def gui_thread():
    layout = [
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Text('Detected Emotion: ', key='-EMOTION-')],
        [sg.Button('Capture Emotion', button_color=('black', 'orange'), key='-CAPTURE-EMOTION-')],
        [sg.Button('Play Song', button_color=('black', 'green'), key='-PLAY-')],
        [sg.Text(size=(30, 1), key='-RETURN-VALUE-')]
    ]

    window = sg.Window('Facial Expression Recognition', layout)

    Thread(target=video_thread, args=(window,), daemon=True).start()

    current_emotion = None  # Store the latest captured emotion

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-CAPTURE-EMOTION-':
            current_emotion = window['-EMOTION-'].DisplayText.split(":")[1].strip()
            window['-RETURN-VALUE-'].update(value=f'Detected Emotion: {current_emotion}')
        elif event == '-PLAY-' and current_emotion:
            play_song_with_emotion(current_emotion, window)

    window.close()

if __name__ == "__main__":
    gui_thread()

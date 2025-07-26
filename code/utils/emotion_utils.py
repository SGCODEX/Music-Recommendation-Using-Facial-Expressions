import numpy as np
import cv2

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(gray_image):
    return face_cascade.detectMultiScale(gray_image, 1.3, 5)

def preprocess_face(roi_gray):
    roi_gray = cv2.resize(roi_gray, (64, 64))
    roi = roi_gray.astype("float") / 255.0
    roi = np.expand_dims(roi, axis=0)
    roi = np.expand_dims(roi, axis=-1)
    return roi

def predict_emotion(model, roi):
    preds = model.predict(roi)[0]
    return emotions[np.argmax(preds)]


import cv2
import numpy as np
import onnxruntime as ort

# Load ONNX model
session = ort.InferenceSession("emotion-ferplus-8.onnx")

# Emotion labels for FER+
emotions = ['neutral', 'happiness', 'surprise', 'sadness',
            'anger', 'disgust', 'fear', 'contempt']

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

print("Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (64, 64))
        face_normalized = face_resized.astype(np.float32) / 255.0
        face_reshaped = face_normalized[np.newaxis, np.newaxis, :, :]

        inputs = {session.get_inputs()[0].name: face_reshaped}
        output = session.run(None, inputs)[0]
        emotion_idx = int(np.argmax(output))
        emotion_label = emotions[emotion_idx]

        # Draw on frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

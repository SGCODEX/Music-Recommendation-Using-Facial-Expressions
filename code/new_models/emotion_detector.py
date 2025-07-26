import cv2
from fer import FER

detector = FER(mtcnn=True)
cap = cv2.VideoCapture(0)

print("Detecting emotions... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = detector.detect_emotions(frame)

    for face in results:
        (x, y, w, h) = face["box"]
        emotions = face["emotions"]
        top_emotion = max(emotions, key=emotions.get)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, top_emotion, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

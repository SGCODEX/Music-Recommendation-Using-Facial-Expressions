import cv2
from ultralytics import YOLO
from deepface import DeepFace


model = YOLO('yolov5s.pt') 

# Start video capture (webcam)
cap = cv2.VideoCapture(0)

# Variable to store the detected emotion
detected_emotion = None

while True:
    # Capture frame-by-frame from webcam
    ret, frame = cap.read()
    
    if not ret:
        break

    # Perform face detection with YOLOv5
    results = model(frame)

    # Get the results from the detection output (results.xyxy is in the predictions)
    for result in results[0].boxes:  # Each result contains bounding boxes
        x1, y1, x2, y2 = result.xyxy[0].tolist()  # Extract the coordinates of the bounding box
        
        if result.conf[0] > 0.5:  # Filter faces with low confidence
            # Crop face from the frame
            face = frame[int(y1):int(y2), int(x1):int(x2)]

            # Use DeepFace for emotion detection
            try:
                # DeepFace will return the emotion with the highest confidence
                analysis = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                detected_emotion = analysis[0]['dominant_emotion']
            except Exception as e:
                print(f"Error in emotion analysis: {e}")
                detected_emotion = "Unknown"
            
            # Draw bounding box and emotion label on face
            label = f"{detected_emotion}"
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Emotion Detection', frame)
    
    # Check for keypress to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Output the detected emotion (for debugging or logging)
    print(f"Detected Emotion: {detected_emotion}")

# Release webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Return the detected emotion
print(f"Final Detected Emotion: {detected_emotion}")

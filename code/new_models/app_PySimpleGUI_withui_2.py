import cv2
import PySimpleGUI as sg
from keras.models import load_model
import numpy as np
import webbrowser
from threading import Thread, Event
import requests
import re
import time

model = load_model('code/model/fer2013_mini_XCEPTION.102-0.66.hdf5')
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
DEFAULT_CAMERA_INDEX = 0

def emoji_for(emotion):
    mapping = {
        'Angry': '😡', 'Disgust': '🤢', 'Fear': '😨', 'Happy': '😄',
        'Sad': '😢', 'Surprise': '😲', 'Neutral': '😐'
    }
    return mapping.get(emotion, '🙂')

def emotion_fill_percentage(emotion):
    levels = {
        'Happy': 100, 'Surprise': 80, 'Neutral': 50,
        'Sad': 30, 'Fear': 20, 'Disgust': 20, 'Angry': 10
    }
    return levels.get(emotion, 50)

def color_for_emotion(emotion):
    mapping = {
        'Happy': ('#1E88E5', '#E3F2FD'),
        'Sad': ('#1976D2', '#E3F2FD'),
        'Angry': ('#D32F2F', '#FFEBEE'),
        'Surprise': ('#0288D1', '#E1F5FE'),
        'Fear': ('#455A64', '#CFD8DC'),
        'Disgust': ('#00796B', '#E0F2F1'),
        'Neutral': ('#5C6BC0', '#E8EAF6')
    }
    return mapping.get(emotion, ('#2196F3', '#E3F2FD'))

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
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 255), 2)
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 120, 255), 2)
        return frame, emotion_label
    return None, None  # Return None when no faces are detected

def play_song_with_emotion(emotion, window):
    search_query = f"https://www.youtube.com/results?search_query={emotion}+weekend+beats"
    response = requests.get(search_query)
    html_content = response.text
    match = re.search(r'/watch\?v=([^\"]+)', html_content)
    if match:
        video_id = match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(video_url)

def video_worker(window, stop_event, cam_idx):
    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        window.write_event_value('-STATUS-', ('Cannot open camera', 'bad'))
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    prev_time = time.time()
    fps = 0.0

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            window.write_event_value('-STATUS-', ('Camera read failed', 'bad'))
            break

        frame = cv2.resize(frame, (640, 480))
        frame_with_faces, detection = detect_emotion(frame, face_cascade)
        frame_to_show = frame_with_faces if frame_with_faces is not None else frame

        now = time.time()
        fps = 1.0 / (now - prev_time) if now != prev_time else fps
        prev_time = now

        imgbytes = cv2.imencode('.png', frame_to_show)[1].tobytes()
        window.write_event_value(
            '-FRAME-',
            {'img': imgbytes, 'emotion': detection, 'fps': fps}
        )

    cap.release()

def build_layout():
    sg.theme('LightBlue2')

    header = [sg.Text('🎵 Music-Recommendation-Using-Facial-Expressions🎵',
                      font=('Helvetica', 18, 'bold'),
                      text_color='#0D47A1',
                      justification='center',
                      expand_x=True,
                      pad=((0,0),(10,10)))]

    camera_panel = [
        [sg.Image(key='-IMAGE-', size=(640, 480))],
        [sg.Text('FPS: --', key='-FPS-', size=(12, 1), text_color='#01579B')]
    ]

    main_panel = [
        [sg.Text('Detected Emotion', font=('Helvetica', 17, 'bold'), text_color='#1565C0')],
        [sg.Text('—', key='-EMOTION-TEXT-', font=('Helvetica', 32, 'bold'), text_color='#1A237E')],
        [sg.ProgressBar(100, orientation='h', size=(30, 15), key='-EMOTION-BAR-', bar_color=('#1565C0', 'white'))],
        [sg.Button(
            '📸 Capture',
            key='-CAPTURE-EMOTION-',
            button_color=('white', '#1E88E5'),  
            mouseover_colors=('white', '#0D47A1'),  
            size=(17, 1),
            font=('Helvetica', 14, 'bold')
        ),
        sg.Button(
            '▶ Play Song',
            key='-PLAY-',
            button_color=('white', '#009688'),   
            mouseover_colors=('white', '#00796B'),
            size=(17, 1),
            font=('Helvetica', 14, 'bold')
        )],
        [sg.Text('', key='-RETURN-VALUE-', size=(45, 1), text_color='#0477BF', font=('Helvetica', 14, 'italic'))]
    ]

    footer = [sg.Text("GSSoC'25", justification='center', expand_x=True, text_color='#1565C0')]

    layout = [
        header,
        [sg.Column(camera_panel, element_justification='center'),
         sg.VSeperator(color='#90A4AE'),
         sg.Column(main_panel, element_justification='center')],
        [sg.HorizontalSeparator(color='#90A4AE')],
        footer
    ]
    return layout

def gui_thread():
    window = sg.Window('Facial Expression Recognition',
                       build_layout(), resizable=True, finalize=True)
    stop_event = Event()
    video_thread = Thread(target=video_worker, args=(window, stop_event, DEFAULT_CAMERA_INDEX), daemon=True)
    video_thread.start()

    current_emotion = None
    window_closed = False

    while True:
        event, values = window.read(timeout=50)

        if event in (sg.WINDOW_CLOSED, sg.WIN_CLOSED):
            stop_event.set()
            window_closed = True
            break

        elif event == '-FRAME-':
            if window_closed:
                continue
            data = values.get('-FRAME-')
            if not data:
                continue
            try:
                window['-IMAGE-'].update(data=data['img'])
                window['-FPS-'].update(f"FPS: {data['fps']:.1f}")
            except Exception:
                continue

            if data['emotion']:
                current_emotion = data['emotion']
                window['-EMOTION-TEXT-'].update(f"{emoji_for(current_emotion)} {current_emotion}")
                window['-EMOTION-BAR-'].update(
                    emotion_fill_percentage(current_emotion),
                    bar_color=color_for_emotion(current_emotion)
                )
            else:
                current_emotion = None
                window['-EMOTION-TEXT-'].update("😶 No face detected")
                window['-EMOTION-BAR-'].update(0)

        elif event == '-CAPTURE-EMOTION-':
            if current_emotion is not None:
                window['-RETURN-VALUE-'].update(
                    value=f"Detected Emotion: {current_emotion}"
                )
            else:
                window['-RETURN-VALUE-'].update('No emotion detected yet.')

        elif event == '-PLAY-':
            if not current_emotion:
                window['-RETURN-VALUE-'].update('Capture an emotion first.')
            else:
                url = play_song_with_emotion(current_emotion, window)
                window['-RETURN-VALUE-'].update(f'Playing: {url}' if url else 'Failed to fetch a YouTube link.')

    stop_event.set()
    video_thread.join(timeout=2.0)
    try:
        window.close()
    except Exception:
        pass

if __name__ == '__main__':
    gui_thread()

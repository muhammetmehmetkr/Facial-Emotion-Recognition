import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import tempfile
from tensorflow import keras

model = keras.models.load_model('best_model.keras')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def process_face(face_image):
    face_image = cv2.resize(face_image, (48, 48))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = np.expand_dims(face_image, axis=-1)
    face_image = np.expand_dims(face_image, axis=0)
    face_image = face_image / 255.0
    return face_image

def update_frame():
    ret, frame = cap.read()

    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # En büyük yüzü belirle
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        (x, y, w, h) = largest_face

        face_image = frame[y:y+h, x:x+w]
        processed_face = process_face(face_image)

        predictions = model.predict(processed_face)
        prediction = np.argmax(predictions[0])
        emotion_label = emotion_labels[prediction]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_image)
    img = ImageTk.PhotoImage(pil_image)
    panel.config(image=img)
    panel.image = img

    root.after(10, update_frame)

cascade_txt_path = r'C:\Users\muham\OneDrive\Masaüstü\archive\pythonProject\haarcascade_frontalface_default.txt'

with open(cascade_txt_path, 'r', encoding='utf-8') as file:
    cascade_xml_content = file.read()

with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
    temp_file.write(cascade_xml_content.encode('utf-8'))
    temp_cascade_path = temp_file.name

face_cascade = cv2.CascadeClassifier(temp_cascade_path)

if face_cascade.empty():
    raise IOError(f"Unable to load the face cascade classifier from the temporary file")

cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Real-time Facial Emotion Recognition")

root.geometry("800x600")

panel = tk.Label(root)
panel.pack()

root.after(10, update_frame)
root.mainloop()

cap.release()
cv2.destroyAllWindows()

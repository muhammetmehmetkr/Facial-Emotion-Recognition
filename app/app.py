import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import tempfile
from tensorflow import keras

model = keras.models.load_model('best_model.keras')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
emotion_scores = {emotion: 0 for emotion in emotion_labels}
attempts_dict = {emotion: 3 for emotion in emotion_labels}

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        load_image(file_path)

def process_face(face_image):
    face_image = cv2.resize(face_image, (48, 48))  # Resize to 48x48
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    face_image = np.expand_dims(face_image, axis=-1)
    face_image = np.expand_dims(face_image, axis=0)
    face_image = face_image / 255.0  # Normalize
    return face_image

def update_score_display():
    score_text = "\n".join([f"{emotion}: {score}" for emotion, score in emotion_scores.items()])
    score_label.config(text=f"Scores:\n{score_text}")

def update_attempts_display():
    attempts_text = "\n".join([f"{emotion}: {attempts}" for emotion, attempts in attempts_dict.items()])
    attempts_label.config(text=f"Attempts:\n{attempts_text}")

def load_image(file_path):
    selected_emotion = emotion_var.get()
    if selected_emotion not in emotion_labels:
        messagebox.showerror("Error", "Please select a valid emotion")
        return

    image = Image.open(file_path)
    image.thumbnail((300, 300))  # Resize image to fit within 300x300

    # Convert image to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Detect faces
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        text_panel.config(text="No faces detected")
        # Show the image even if no face is detected
        pil_image = image
    else:
        # Find the largest face
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face

        face_image = cv_image[y:y+h, x:x+w]
        processed_face = process_face(face_image)

        # Predict emotion
        predictions = model.predict(processed_face)
        prediction = np.argmax(predictions[0])
        emotion_label = emotion_labels[prediction]

        # Draw rectangle around the largest face
        cv_image = cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert image back to PIL format
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        # Display emotion below the image
        text_panel.config(text=f"Predicted Emotion: {emotion_label}\nYour Emotion: {selected_emotion}")

        # Check if the user's guess is correct
        if selected_emotion == emotion_label:
            emotion_scores[selected_emotion] += 1
            #messagebox.showinfo("Result", f"Correct! Your score for {selected_emotion} is now: {emotion_scores[selected_emotion]}")
            if emotion_scores[selected_emotion] >= 7:
                messagebox.showinfo("Congratulations", f"Tebrikler kazandınız! {selected_emotion} puanı 7'ye ulaştı!")
                root.destroy()  # Finish program
                return
        else:
            attempts_dict[selected_emotion] -= 1
            if attempts_dict[selected_emotion] == 0:
                messagebox.showinfo("Game Over", f"Kaybettiniz! All attempts for {selected_emotion} are used up.")
                root.destroy()
                return
            #messagebox.showinfo("Result", f"Incorrect! The correct emotion was: {emotion_label}")

    # Display the image
    img = ImageTk.PhotoImage(pil_image)
    panel.config(image=img)
    panel.image = img

    update_score_display()
    update_attempts_display()

# Specify the path to the txt file
cascade_txt_path = r'C:\Users\muham\OneDrive\Masaüstü\archive\pythonProject\haarcascade_frontalface_default.txt'

# Read the contents of the file and write it to a temporary XML file
with open(cascade_txt_path, 'r', encoding='utf-8') as file:
    cascade_xml_content = file.read()

# Create a temporary file and write the XML content
with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
    temp_file.write(cascade_xml_content.encode('utf-8'))
    temp_cascade_path = temp_file.name

# Load the pre-trained face detection model from the temporary file
face_cascade = cv2.CascadeClassifier(temp_cascade_path)

# Check if the cascade file is loaded properly
if face_cascade.empty():
    raise IOError(f"Unable to load the face cascade classifier from the temporary file")

# Create the main window
root = tk.Tk()
root.title("Facial Emotion Recognition")

# Set initial size of the window
root.geometry("750x600")

# Create a Combobox for emotion selection
emotion_var = tk.StringVar()
emotion_combobox = ttk.Combobox(root, textvariable=emotion_var, state="readonly")
emotion_combobox['values'] = emotion_labels
emotion_combobox.set("Select Emotion")
emotion_combobox.pack(pady=10)

# Create a button to open the file dialog
btn = tk.Button(root, text="Select Photo", command=open_file)
btn.pack(pady=10)

# Create a panel to display the image
panel = tk.Label(root)
panel.pack()

# Create a panel to display the emotions
text_panel = tk.Label(root, text="", font=("Helvetica", 14))
text_panel.pack()

# Create a label to display the scores
score_label = tk.Label(root, text="", font=("Helvetica", 12))
score_label.pack(side="left", anchor="s", padx=20)

# Create a label to display the attempts
attempts_label = tk.Label(root, text="", font=("Helvetica", 12))
attempts_label.pack(side="right", anchor="s", padx=20)

# Start the GUI event loop
update_score_display()
update_attempts_display()
root.mainloop()

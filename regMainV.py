import os.path
import datetime
import pickle

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import util


# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a8879-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-a8879.appspot.com"
})

#creating the window
class App:

    def __init__(self):
        self.name = ""
        self.major = ""
        self.starting_year = ""
        self.standing = ""
        self.current_year = ""
        self.main_window = None
    
    def register_new_user(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.configure(bg='white')  # Set the background color to white

        # Add registration topic label
        self.registration_topic_label = tk.Label(self.main_window, text="REGISTRATION", font=('Arial Narrow', 30))
        self.registration_topic_label.place(x=830, y=100)

        # Add entry fields for user information
        self.name_label = tk.Label(self.main_window, text="Name: ", font=('Arial', 12), bg='white', fg='black')
        self.name_label.place(x=800, y=200)
        self.name_entry = tk.Entry(self.main_window, font=('Arial', 12))
        self.name_entry.place(x=900, y=200)

        self.major_label = tk.Label(self.main_window, text="Major: ", font=('Arial', 12), bg='white', fg='black')
        self.major_label.place(x=800, y=250)
        self.major_entry = tk.Entry(self.main_window, font=('Arial', 12))
        self.major_entry.place(x=900, y=250)

        self.starting_year_label = tk.Label(self.main_window, text="Starting Year: ", font=('Arial', 12), bg='white', fg='black')
        self.starting_year_label.place(x=800, y=300)
        self.starting_year_entry = tk.Entry(self.main_window, font=('Arial', 12))
        self.starting_year_entry.place(x=900, y=300)

        self.standing_label = tk.Label(self.main_window, text="Standing (g/b): ", font=('Arial', 12), bg='white', fg='black')
        self.standing_label.place(x=800, y=350)
        self.standing_entry = tk.Entry(self.main_window, font=('Arial', 12))
        self.standing_entry.place(x=900, y=350)

        self.current_year_label = tk.Label(self.main_window, text="Current Year: ", font=('Arial', 12), bg='white', fg='black')
        self.current_year_label.place(x=800, y=400)
        self.current_year_entry = tk.Entry(self.main_window, font=('Arial', 12))
        self.current_year_entry.place(x=900, y=400)

        # Add buttons for capturing photo and retrying
        #self.submit_info_button = tk.Button(self.main_window, text="Submit", font=('Arial', 16), command=self.capture_photo, bg='green', fg='white')
        self.submit_info_button = tk.Button(self.main_window, text="Submit", font=('Arial', 16), bg='green', fg='white',command=self.submit_info)
        self.submit_info_button.place(x=950, y=450)

        #self.retry_button = tk.Button(self.main_window, text="Try Again", font=('Arial', 12))
        #self.retry_button.place(x=920, y=450)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)  # Modify the camera index if needed

            self._label = label
            self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    #def capture_photo(self):
        #username = self.entry_text_take_photo_window.get()  # Get the username from the entry field
        #self.submit_info_button.config(state='disabled')  # Disable the photo button temporarily
        #self.retry_button.config(state='disabled')  # Disable the retry button temporarily


    def submit_info(self):

        name = self.name_entry.get()
        major = self.major_entry.get()
        starting_year = self.starting_year_entry.get()
        standing = self.standing_entry.get()
        current_year = self.current_year_entry.get()

        # Create a dictionary with user information
        user_info = {
            'name': name,
            'major': major,
            'starting_year': starting_year,
            'standing': standing,
            'current_year': current_year,
            'last_attendance_time':'2022-12-11 00:54:34'
    }
        
        # Save the user information to the Firebase Realtime Database
        ref = db.reference('Students')
        new_user_ref = ref.push()
        new_user_ref.set(user_info)

        # Reset the entry fields
        self.name_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)
        self.starting_year_entry.delete(0, tk.END)
        self.standing_entry.delete(0, tk.END)
        self.current_year_entry.delete(0, tk.END)


        self.take_photo_window = tk.Toplevel(self.main_window)
        self.take_photo_window.geometry("1200x520+370+120")

        self.photo_button_take_photo_window = util.get_button(self.take_photo_window, 'Accept', 'green', self.photo_take_photo)
        self.photo_button_take_photo_window.place(x=750, y=300)

        self.try_again_button_take_photo_window = util.get_button(self.take_photo_window, 'Try Again', 'red',self.try_again_take_photo)
        self.try_again_button_take_photo_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.take_photo_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def photo_take_photo(self):
        name = self.name_entry.get()
        embeddings = face_recognition.face_encodings(self.register_new_user_capture)

        # Create the "images" folder if it doesn't exist
        images_folder = os.path.join(os.getcwd(), "Images")
        if not os.path.exists(images_folder):
            os.mkdir(images_folder)
        
        if len(embeddings) == 0:
            util.msg_box('Error', 'No face detected. Please try again.')
            return
        else:
            # Save the captured image with the user's name
            image_file_path = os.path.join(images_folder, '{}.jpg'.format(name))
            cv2.imwrite(image_file_path, self.register_new_user_capture)
            util.msg_box('Success!', 'User was registered successfully!')

        

        self.take_photo_window.destroy()

        
    def try_again_take_photo(self):
        self.take_photo_window.destroy()

    def start(self):
        self.register_new_user()
        self.main_window.mainloop()

if __name__=="__main__":
    app = App()
    #app.register_new_user()
    app.start()
    

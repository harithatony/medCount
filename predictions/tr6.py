
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import cv2
from list3 import YOLO_Pred
import pyttsx3
from tr4 import count_instruments, check, speak_warning_message,add_patient_to_excel
yolo = YOLO_Pred('./Model/weight/best.onnx','data_yaml') 
import pandas as pd
class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Med Count")
        self.geometry("900x900")
        self.configure(bg="black")

        self.login_frame = ttk.Frame(self)
        self.patient_frame = ttk.Frame(self)
        self.image_frame = ttk.Frame(self)
        

        self.add_login_area()
        self.add_patient_detail_area()
        self.show_login_area()

        self.selected_images = {'before': [], 'after': []}
        self.compare_result = None
        self.staff_data = pd.read_excel("staff_data.xlsx")
        

    
    def add_login_area(self):
        
        self.login_frame = ttk.Frame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configure style for login frame
        style = ttk.Style()
        style.configure("TFrame", background="black")

        # Welcoming label
        ttk.Label(self.login_frame, text="Welcome to Royal Hospital", foreground="white", background="black",font=("Comic Sans MS",20)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Username:", foreground="white", background="black").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Password:", foreground="white", background="black").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.error_label = ttk.Label(self.login_frame, text="", foreground="red", background="black")
        self.error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.authenticate)
        self.login_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


    def add_patient_detail_area(self):
        
        ttk.Label(self.patient_frame, text="Royal Hospital", foreground="white", background="black",font=("Comic Sans MS",20)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
    
        ttk.Label(self.patient_frame, text="Patient Name:",foreground="white", background="black").grid(row=1, column=0, padx=5, pady=5)
        self.patient_name_entry = ttk.Entry(self.patient_frame)
        self.patient_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.patient_frame, text="Doctor Name:",foreground="white", background="black").grid(row=2, column=0, padx=5, pady=5)
        self.doctor_name_entry = ttk.Combobox(self.patient_frame, values=["Dr. Nick", "Dr. Jhon", "Dr. Marcus"])  # Example dropdown values
        self.doctor_name_entry.grid(row=2, column=1, padx=5, pady=5)

        self.error_label = ttk.Label(self.patient_frame, text="", foreground="red", background="black")
        self.error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


        self.patient_button = ttk.Button(self.patient_frame, text="Submit", command=self.toggle_to_camera)
        self.patient_button.grid(row=4, columnspan=2, padx=5, pady=5)
        # Add logout button
        self.logout_button = ttk.Button(self.patient_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=5, columnspan=2, padx=5, pady=5)
            
    def show_camera_area(self):
        self.patient_frame.grid_forget()
        self.image_frame.grid_forget()
        ttk.Label(self.image_frame, text="Royal Hospital",foreground="white", background="black",font=("Comic Sans MS",20)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
       
        ttk.Label(self.image_frame, text=f"Staff Name: {self.username_entry.get()}", foreground="white", background="black", font=("Georgia", 14)).grid(row=0, column=5, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Label(self.image_frame, text=f"Doctor Name : {self.doctor_name_entry.get()}", foreground="white", background="black", font=("Georgia", 14)).grid(row=1, column=5, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Label(self.image_frame, text=f"Patient Name: {self.patient_name_entry.get()}", foreground="white", background="black", font=("Georgia", 14)).grid(row=2, column=5, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Label(self.image_frame, text=f"Surgery Status: None", foreground="white", background="black", font=("Georgia", 14)).grid(row=3, column=5, columnspan=2, padx=5, pady=5, sticky="w")

        ttk.Label(self.image_frame, text="Before Surgery",foreground="white", background="black").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.image_frame, text="After Surgery",foreground="white", background="black").grid(row=1, column=1, padx=5, pady=5)

        self.before_image_labels = []
        self.after_image_labels = []

        for i in range(5):
            before_label = ttk.Label(self.image_frame, background="black")
            before_label.grid(row=i+3, column=0, padx=5, pady=5)
            self.before_image_labels.append(before_label)

            after_label = ttk.Label(self.image_frame, background="black")
            after_label.grid(row=i+3, column=1, padx=5, pady=5)
            self.after_image_labels.append(after_label)

        self.before_count_labels = [ttk.Label(self.image_frame, text="",foreground="white", background="black") for _ in range(5)]
        for i, label in enumerate(self.before_count_labels):
            label.grid(row=i+3, column=0, sticky="n", padx=5)

        self.after_count_labels = [ttk.Label(self.image_frame, text="",foreground="white", background="black") for _ in range(5)]
        for i, label in enumerate(self.after_count_labels):
            label.grid(row=i+3, column=1, sticky="n", padx=5)

        self.before_buttons = []
        self.after_buttons = []

        for i in range(5):
            before_button = ttk.Button(self.image_frame, text=f"Select Before Image {i+1}",
                                       command=lambda index=i: self.select_image('before', index))
            before_button.grid(row=i+8, column=0, padx=5, pady=5)
            self.before_buttons.append(before_button)

            after_button = ttk.Button(self.image_frame, text=f"Select After Image {i+1}",
                                      command=lambda index=i: self.select_image('after', index))
            after_button.grid(row=i+8, column=1, padx=5, pady=5)
            self.after_buttons.append(after_button)

        self.compare_button = ttk.Button(self.image_frame, text="Compare", command=self.compare)
        self.compare_button.grid(row=15, columnspan=3, padx=5, pady=5)

        self.image_frame.grid(row=0, column=0, padx=5, pady=5)
        # Add logout button
        self.logout_button = ttk.Button(self.image_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=17, columnspan=3, padx=5, pady=5)

    def select_image(self, button_type, index):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = cv2.imread(file_path)
            print(file_path)
            img, d = self.count_instruments(file_path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB format
                img = cv2.resize(img, (200, 200))  # Resize image for display
                
                if button_type == 'before':
                    self.before_image_labels[index].img = ImageTk.PhotoImage(Image.fromarray(img))
                    self.before_image_labels[index].config(image=self.before_image_labels[index].img)
                    self.selected_images['before'].append(file_path)
                    self.before_count_labels[index].config(text=f"Count: {d}")
                    self.before_buttons[index].config(state=tk.DISABLED)
                    self.beforelist.append(d)
                elif button_type == 'after':
                    self.after_image_labels[index].img = ImageTk.PhotoImage(Image.fromarray(img))
                    self.after_image_labels[index].config(image=self.after_image_labels[index].img)
                    self.selected_images['after'].append(file_path)
                    self.after_count_labels[index].config(text=f"Count: {d}")
                    self.after_buttons[index].config(state=tk.DISABLED)
                    self.afterlist.append(d)
            else:
                print("Error: Unable to load image file.")


    def count_instruments(self, img):
        return count_instruments(img)
    

    def compare(self):
        self.print_details()
        print(self.beforelist,self.afterlist)
        difference = check(self.beforelist,self.afterlist)
        if len(difference) == 0:
            msg = "surgery succesful"
            speak_warning_message(msg)
            # ttk.Label(self.image_frame, text="  Surgery Successful  ",foreground="white", background="black").grid(row=12, column=2, padx=5, pady=5)
            ttk.Label(self.image_frame, text=f"Surgery Status: Successful", foreground="green", background="black", font=("Georgia", 14)).grid(row=3, column=5, columnspan=2, padx=5, pady=5, sticky="w")
            patient_name = self.patient_name_entry.get()
            doctor_name = self.doctor_name_entry.get()
            staff_name = self.username_entry.get()
            status = "Successful"
            add_patient_to_excel(patient_name,doctor_name,staff_name,status)

            try:
                self.difference_label.after(1000, self.difference_label.destroy())
                self.diff_label.after(1000, self.diff_label.destroy())
            except AttributeError:
                pass
        else:
            msg = ""
            for i in difference:
                msg += str(i) +" "+ str(difference[i]) +" "
            msg += " are missing"
            print(msg)
            speak_warning_message(msg)
            diff = ""
            for i in difference:
                diff += i + " - " + str(difference[i]) +"\n"
            self.diff_label = ttk.Label(self.image_frame, text=f"Instruments missing:", foreground="red", background="black", font=("Georgia", 14))
            self.diff_label.grid(row=4, column=5, columnspan=2, padx=5, pady=5, sticky="w")
            self.difference_label = ttk.Label(self.image_frame, text=f"{diff}",foreground="blue", background="black",font=("Trebuchet MS",16))
            self.difference_label.grid(row=5, column=5, padx=5, pady=5,sticky="w")
            ttk.Label(self.image_frame, text=f"Surgery Status: Missing    ", foreground="red", background="black", font=("Georgia", 14)).grid(row=3, column=5, columnspan=2, padx=5, pady=5, sticky="w")
            patient_name = self.patient_name_entry.get()
            doctor_name = self.doctor_name_entry.get()
            staff_name = self.username_entry.get()
            status = "Missing"
            add_patient_to_excel(patient_name,doctor_name,staff_name,status)

            
            
    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are in staff data
        if any((self.staff_data['username'] == username) & (self.staff_data['password'] == password)):
            print("Login successful")
            self.show_patient_detail_area()
            # Call a method to show the patient detail area
            
        else:
            self.error_label.config(text="Invalid username or password")


    def toggle_to_camera(self):
    # Get patient name and doctor name from the entry fields
        patient_name = self.patient_name_entry.get()
        doctor_name = self.doctor_name_entry.get()
        staff_name = self.username_entry.get()

        # Check if any field is empty
        if not (patient_name and doctor_name):
            # If any field is empty, display an error message
            self.error_label.config(text="Enter patient and doctor details")
        else:
            # If all fields are filled, clear the error message
            self.error_label.config(text="")
            self.afterlist = []
            self.beforelist = []
            # add_patient_to_excel(patient_name,doctor_name,staff_name)
            self.show_camera_area()


    def show_login_area(self):
        self.patient_frame.grid_forget()
        self.image_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, padx=5, pady=5)
        self.login_button["text"] = "Login"

    def show_patient_detail_area(self):
        self.image_frame.grid_forget()
        self.login_frame.grid_forget()
        self.patient_frame.grid(row=0, column=0, padx=5, pady=5)
        self.login_button["text"] = "Back"

    def print_details(self):
        if self.patient_name_entry.get() and self.doctor_name_entry.get():
            print("Username:", self.username_entry.get())
            print("Password:", self.password_entry.get())
            print("Patient Name:", self.patient_name_entry.get())
            print("Doctor Name:", self.doctor_name_entry.get())
        else:
            print("Please enter patient name and doctor name.")
    def logout(self):
        # Hide other frames
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.patient_name_entry.delete(0, 'end')
        self.doctor_name_entry.delete(0, 'end')
        for index in range(5):
            try:
                self.before_image_labels[index].config(image=None)  # Remove the image
                self.before_buttons[index].config(state=tk.NORMAL) 
            except:
                pass
            try:
                self.after_image_labels[index].config(image=None)  # Remove the image
                self.after_buttons[index].config(state=tk.NORMAL)  # Enable the button
            except:
                pass
        self.before_image_labels = []
        self.after_image_labels = []
        self.afterlist = []
        self.beforelist = []

        self.login_frame.grid_forget()
        self.patient_frame.grid_forget()
        self.image_frame.grid_forget()
        # Show login frame
        self.show_login_area()
    def remove_labels(self, *labels):
        for label in labels:
            label.grid_forget()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()

import streamlit as st
import cv2
from PIL import Image
import numpy as np
from st2 import count_instruments, check

# Function to simulate login
def login(username, password):
    # Simulate a simple login check
    # if username == "user" and password == "password":
    if username == "" and password == "":
        return True
    else:
        return False

# Login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
            st.session_state.username = username
            return True
        else:
            st.error("Invalid username or password. Please try again.")
            return False

# Page after successful login
def main_page():
    st.title("Royal Hospital")
    username = st.session_state.username
    st.write(f"Welcome {username}!")
    patient_name = st.text_input("Patient name", "")
    st.session_state.patient = patient_name
    doctor_name = st.selectbox("Doctor's Name", ["Select Doctor","Dr. Ambaan", "Dr. Ranga", "Dr. Appi Biju"])
    st.session_state.doctor = doctor_name
    if st.button("Proceed"):
    #     if patient_name == "" or doctor_name == "Select Doctor":
    #         st.error("Invalid Patient/Doctor name!!!")
    #     else:
    #         return True
        return True
    
def count_page():
    before_list=[]
    after_list =[]
    user = st.session_state.username
    patient = st.session_state.patient
    doctor = st.session_state.doctor
    st.title("Royal Hospital")
    st.subheader(f"Staff Name : {user}")
    st.subheader(f"Patient Name : {patient}")
    st.subheader(f"Doctor Name : {doctor}")
    # Create two columns
    col1, col2 = st.columns(2)
    # Function to display uploaded images
    def display_uploaded_images(uploaded_files, col,name):
        dicts={}
        for uploaded_file in uploaded_files:
            with col:
                if uploaded_file is not None:
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    bw_img,dicts = count_instruments(file_bytes)
                    b = ""
                    for i in dicts:
                        b+=str(i)+":"+str(dicts[i])+"\n"
                    st.image(bw_img, caption=b,width=200)  
        return dicts
    # Upload images for the first column
    with col1:
        st.header("Before Surgery")
        uploaded_files_col1_1 = [st.file_uploader(f"Before Surgery1", type=["jpg", "jpeg", "png"])]
        before = "Before Image"
        print("hai")
        before_list.append(display_uploaded_images(uploaded_files_col1_1, col1,before))
        uploaded_files_col1_2 = [st.file_uploader(f"Before Surgery2", type=["jpg", "jpeg", "png"])]
        before = "Before Image"
        before_list.append(display_uploaded_images(uploaded_files_col1_2, col1,before))
        uploaded_files_col1_3 = [st.file_uploader(f"Before Surgery3", type=["jpg", "jpeg", "png"])]
        before = "Before Image"
        before_list.append(display_uploaded_images(uploaded_files_col1_3, col1,before))

    # Upload images for the second column
    with col2:
        st.header("After Surgery")
        uploaded_files_col2_1 = [st.file_uploader(f"After Surgery1", type=["jpg", "jpeg", "png"])]
        after = "After Image"
        after_list.append(display_uploaded_images(uploaded_files_col2_1, col2,after))
        uploaded_files_col2_2 = [st.file_uploader(f"After Surgery2", type=["jpg", "jpeg", "png"])]
        after = "After Image"
        after_list.append(display_uploaded_images(uploaded_files_col2_2, col2,after))
        uploaded_files_col2_3 = [st.file_uploader(f"After Surgery3", type=["jpg", "jpeg", "png"])]
        after = "After Image"
        after_list.append(display_uploaded_images(uploaded_files_col2_3, col2,after))


    if st.button("compare"):
        print(before_list,after_list)
        diff =check(before_list,after_list)
        if diff:
            st.write("Surgery Status : Missing")
            b = ""
            for i in diff:
                 b+=str(i)+":"+str(diff[i])+" "
            st.write("Missing Instruments :" ,b)
        else:
            st.write("Surgery Status : Successful")

# Main function to control navigation
def main():
    page = st.session_state.get("page", "login")

    if page == "login":
        if login_page():
            st.session_state.page = "main"
    elif page == "main":
        if main_page():
            st.session_state.page = "count"
    elif page == "count":
        count_page()

if __name__ == "__main__":
    main()
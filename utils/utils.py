import os
import shutil
import datetime
from PIL import Image, ImageTk
import itertools
import time
import sys

CURRENT_VERSION_FILE = "C:\\Check_All_Stage\\version.txt"

is_animating = False

def get_data_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, relative_path)
    if not os.path.exists(data_path):
        install_path = r"C:\Check_All_Stage"
        data_path = os.path.join(install_path, relative_path)
    return data_path

def get_current_version():
    if os.path.exists(CURRENT_VERSION_FILE):
        with open(CURRENT_VERSION_FILE, "r") as file:
            return file.read().strip()
    return "0.0.0"

def show_image(label, image_path):
    global is_animating
    is_animating = False 
    try:
        if not label.winfo_exists():
            return
        img = Image.open(image_path)
        img = img.resize((60, 60), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
    except:
        pass

def show_image_narrow(label, image_path):
    global is_animating
    is_animating = False 
    try:
        if not label.winfo_exists():
            return
        img = Image.open(image_path)
        img = img.resize((30, 30), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
    except:
        pass

def show_image_mes(label, image_path):
    global is_animating
    is_animating = False 
    try:
        if not label.winfo_exists():
            return
        img = Image.open(image_path)
        img = img.resize((20, 20), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
    except:
        pass

def show_image1(label, image_path):
    global is_animating
    is_animating = True  
    img = Image.open(image_path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(img.copy().resize((200, 200), Image.LANCZOS)))
            img.seek(len(frames))  # Tìm đến frame tiếp theo
    except EOFError:
        pass

    def update_frame(frame_index):
        if not is_animating:  
            return
        try:
            if not label.winfo_exists():
                return
            frame = frames[frame_index]
            label.config(image=frame)
            label.image = frame
            frame_index = (frame_index + 1) % len(frames)
            label.after(100, update_frame, frame_index)
        except:
            pass
    update_frame(0)
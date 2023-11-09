from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import time
import os
import threading
from tkinter import messagebox
import re
import run

global_file_path_undetected = ""
global_file_path_detected = ""
global_file_name = ""
global_frame_numbers = 0
global_average_frame = 0
global_current_frame = 0

file_open = False
video_paused = False  # Track video pause state

# Define a variable for the video capture
cap = None

# Set the desired frame rate (e.g., 30 frames per second)
desired_frame_rate = 30

# Set the playback speed factor
playback_speed_factor = 1.5  # 1.5 normal speedsme

root = Tk()
# root.attributes("-fullscreen", True)
root.title("YOLOv7 + DeepSORT License Plate Coding Detection (CPS - Proof of Concept)")

selected_option = StringVar()
# Create a variable to store the selected number
selected_number = StringVar()
selected_number.set("0")

frm = ttk.Frame(root, padding=20)
frm.pack()

ttk.Label(
    frm,
    text="YOLOv7 + DeepSORT License Plate Coding Detection (CPS - Proof of Concept)",
).pack(padx=10, pady=2)


def update_image(result_rgb):
    photo = ImageTk.PhotoImage(image=Image.fromarray(result_rgb))
    video_label.configure(image=photo)
    video_label.image = photo


def start_timer():
    global start_time
    start_time = time.time()
    update_timer()


def stop_timer():
    time_label.after_cancel(timer_id)


def update_timer():
    elapsed_time = round(time.time() - start_time, 2)
    time_label.config(text=f"DETECTION TIME ELAPSED: {elapsed_time} seconds")
    global timer_id
    timer_id = time_label.after(
        100, update_timer
    )  # Update every 100 milliseconds (0.1 seconds)


def update_text(status, output, average):
    global global_average_frame, global_current_frame
    if status != 0:
        status_label.config(text=status)
    if output != 0:
        output_label.config(text=output)
    if average != 0:
        average_label.config(text=average)


def close_window():
    root.quit()
    root.destroy()


def confirm_run():
    result = messagebox.askyesno("Confirmation", "Begin the detection?")
    if result:
        # Add your code to proceed with the action here
        run_model()


    
def confirm_stop():
    result = messagebox.askyesno("Confirmation", "Stop the detection?")
    if result:
        run_model.stops()
        

        
# Add Pause and Play buttons
def pause_video():
    global video_paused
    video_paused = True


def play_video():
    global video_paused
    if cap is not None:
        video_paused = False
        while not video_paused:
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (480, 270))
            photo = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            video_label.config(image=photo)
            video_label.image = photo
            root.update()
            time.sleep(
                1 / (desired_frame_rate * playback_speed_factor)
            )  # Adjust playback speed


def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the X and Y coordinates for the center of the screen
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to center it on the screen
    window.geometry(f"{width}x{height}+{x}+{y}")

def close_loading():
    close_button["state"] = NORMAL
    run_button["state"] = NORMAL
    status_label.config(text=f"DETECTION STATUS: Detection Complete")
    stop_timer()

    messagebox.showinfo(
        "Complete",
        f"Video Inference Complete. Video with detections saved locally.",
    )

def run_model():
    selected_value = selected_option.get()

    status_label.config(text=f"DETECTION STATUS: Loading YOLOv7 + DeepSORT Model...")
    pause_video()

    print(f"Selected radio option: {selected_value}")
    run_button["state"] = DISABLED

    thread = threading.Thread(
    target=run.run,
        args=(
            global_file_path_undetected,
            global_file_name,
            close_loading,
            start_timer,
            stop_timer,
            update_text,
            update_image,
            selected_number,
        ),
    )
    thread.daemon = True
    thread.start()
    
def open_file():
    global cap, file_open, global_frame_numbers
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("MP4 Files", ("*.mp4")),
            # ("Video Files", ("*.mp4", "*.avi", "*.mkv")),
            # ("Image Files", ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp")),
        ]
    )
    file_open = True
    global global_file_path_undetected, global_file_name
    global_file_path_undetected = file_path
    global_file_name = os.path.basename(file_path)
    if file_path:
        if cap is not None:
            cap.release()  # Release the previous video capture, if any
        if file_path.lower().endswith((".mp4", ".avi", ".mkv")):
            # If the selected file is a video
            cap = cv2.VideoCapture(file_path)
            global_frame_numbers = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_label.config(text=f"VIDEO FRAMES: {global_frame_numbers} frames")
            cap.set(cv2.CAP_PROP_FPS, desired_frame_rate)
            run_button["state"] = NORMAL
            play_video()
        video_name_label.config(text=f"Video File Path: {file_path}")


# def on_select(event):
#     selected_value = selected_number.get()
#     skip_label.config(text=f"Skip every {selected_value}th Frame")


image_label = ttk.Label(frm)
image_label.pack()

video_label = ttk.Label(frm)
video_label.pack()

video_name_label = ttk.Label(frm)
video_name_label.pack()

btn_open = ttk.Button(frm, text="Import Video File (mp4 format)", command=open_file)
btn_open.pack(padx=10, pady=2)

status_label = ttk.Label(frm, text="DETECTION STATUS: Inactive")
status_label.pack(anchor="e", padx=10, pady=2)

time_label = ttk.Label(frm, text="DETECTION TIME ELAPSED: --s")
time_label.pack(anchor="e", padx=10, pady=2)

frame_label = ttk.Label(frm, text="VIDEO FRAMES: --")
frame_label.pack(anchor="e", padx=10, pady=2)

average_label = ttk.Label(frm, text="MODEL AVG. DETECTION TIME PER FRAME: -- FPS")
average_label.pack(anchor="e", padx=10, pady=2)

output_label = ttk.Label(frm, text="")
output_label.pack(padx=10, pady=2)

# skip_label = ttk.Label(frm, text="Skip Every nth Frame (0 Default)")
# skip_label.pack(padx=10, pady=2)

# # Create a dropdown menu with numbers
# number_choices = [str(i) for i in range(0, 6) if i != 1]
# number_dropdown = ttk.Combobox(
#     frm, textvariable=selected_number, values=number_choices, state="readonly"
# )
# number_dropdown.pack()

# number_dropdown.bind("<<ComboboxSelected>>", on_select)

run_button = ttk.Button(
    frm, text="Run License Plate Coding Detection", command=confirm_run, state=DISABLED
)
run_button.pack(padx=10, pady=2)

# stop_button = ttk.Button(
#     frm, text="Stop Detection", command=confirm_stop)
# stop_button.pack(padx=10, pady=2)

close_button = ttk.Button(frm, text="End Detection and Exit Application", command=close_window)
close_button.pack(padx=10, pady=2)


root.mainloop()

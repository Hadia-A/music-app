import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pygame import mixer
import time
from mutagen.mp3 import MP3

# Initialize the music player
def init_music_player():
    mixer.init()

# Load music files from the specified directory
def load_music_library():
    audio_directory = filedialog.askdirectory(title="Select Audio Library Folder")
    if audio_directory:
        for root, dirs, files in os.walk(audio_directory):
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    playlist_box.insert(tk.END, file_path)

# Play selected music
def play_music():
    global paused
    paused = False
    song = playlist_box.get(tk.ACTIVE)
    mixer.music.load(song)
    mixer.music.play()
    
    show_details(song)

# Stop the music
def stop_music():
    mixer.music.stop()
    status_bar.config(text="Music Stopped")
    progress_bar['value'] = 0

# Pause the music
def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    status_bar.config(text="Music Paused")

# Resume the music
def resume_music():
    global paused
    if paused:
        mixer.music.unpause()
        paused = False
        status_bar.config(text="Music Resumed")

# Exit the application
def exit_music_player():
    confirm_exit = messagebox.askyesno("Exit", "Do you really want to exit?")
    if confirm_exit:
        stop_music()
        root.destroy()

# Volume control
def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

# Show song details
def show_details(song):
    file_data = os.path.splitext(song)
    
    if file_data[1] == ".mp3":
        audio = MP3(song)
        total_length = audio.info.length
    else:
        total_length = mixer.Sound(song).get_length()
    
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = "{:02d}:{:02d}".format(mins, secs)
    song_length_label.config(text="Length: " + time_format)
    
    update_progress_bar(total_length)
    
    status_bar.config(text="Playing: " + os.path.basename(song))

# Update progress bar
def update_progress_bar(length):
    progress_bar['maximum'] = length
    current_time = 0
    
    while current_time <= length and mixer.music.get_busy():
        if not paused:
            current_time += 1
            mins, secs = divmod(current_time, 60)
            time_format = "{:02d}:{:02d}".format(mins, secs)
            current_time_label.config(text="Current Time: " + time_format)
            progress_bar['value'] = current_time
            root.update()
            time.sleep(1)

# Initialize the main window
root = tk.Tk()
root.title("Python Music Player")
root.geometry("600x450")
root.config(bg="#f7f7f7")

# Playlist box
playlist_box = tk.Listbox(root, bg="white", fg="black", selectbackground="#a1c4fd", selectforeground="black", width=50, height=15)
playlist_box.pack(pady=20)

# Control buttons
control_frame = tk.Frame(root, bg="#f7f7f7")
control_frame.pack()

play_button = tk.Button(control_frame, text="Play", command=play_music, width=10, bg="#90ee90", fg="black")
play_button.grid(row=0, column=1, padx=10)

pause_button = tk.Button(control_frame, text="Pause", command=pause_music, width=10, bg="#ffd700", fg="black")
pause_button.grid(row=0, column=2, padx=10)

resume_button = tk.Button(control_frame, text="Resume", command=resume_music, width=10, bg="#add8e6", fg="black")
resume_button.grid(row=0, column=3, padx=10)

stop_button = tk.Button(control_frame, text="Stop", command=stop_music, width=10, bg="#ff6961", fg="white")
stop_button.grid(row=0, column=4, padx=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Volume control
volume_frame = tk.Frame(root, bg="#f7f7f7")
volume_frame.pack()

volume_label = tk.Label(volume_frame, text="Volume", bg="#f7f7f7", fg="black")
volume_label.grid(row=0, column=0, padx=20)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, bg="#f7f7f7", fg="black")
volume_slider.set(70)
volume_slider.grid(row=0, column=1, pady=10)

# Song details
details_frame = tk.Frame(root, bg="#f7f7f7")
details_frame.pack()

song_length_label = tk.Label(details_frame, text="Length: --:--", bg="#f7f7f7", fg="black")
song_length_label.grid(row=0, column=0, padx=20)

current_time_label = tk.Label(details_frame, text="Current Time: --:--", bg="#f7f7f7", fg="black")
current_time_label.grid(row=0, column=1, padx=20)

# Status bar
status_bar = tk.Label(root, text="Welcome to Python Music Player", relief=tk.SUNKEN, anchor=tk.W, bg="#f7f7f7", fg="black")
status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Music Library", command=load_music_library)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_music_player)

# Initialize the mixer
init_music_player()

# Run the GUI loop
root.mainloop()

from tkinter import *
import pygame
from tkinter import filedialog
from tkinter import PhotoImage
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title('Silakbo mp3')
root.config(bg = "#374045")
root.iconbitmap('c:/pld/aa.ico')
root.resizable(width=FALSE, height=FALSE)
root.geometry("600x440")


# Initialze Pygame Mixer
pygame.mixer.init()



# FUNCTIONS -----------------------------------------------------


# Grab Song Length Time Info
def play_time():
	# Check for double timing
	if stopped:
		return 
	# Grab Current Song Elapsed Time
	current_time = pygame.mixer.music.get_pos() / 1000

	# throw up temp label to get data
	#slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Get Currently Playing Song
	#current_song = song_box.curselection()
	#Grab song title from playlist
	song = song_box.get(ACTIVE)
	# add directory structure and mp3 to song title
	song = f'C:/pld/audio/{song}.mp3'
	# Load Song with Mutagen
	song_mut = MP3(song)
	# Get song Length
	global song_length
	song_length = song_mut.info.length
	# Convert to Time Format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	# Increase current time by 1 second
	current_time +=1
	
	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
	elif paused:
		pass
	elif int(my_slider.get()) == int(current_time):
		# Update Slider To position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))

	else:
		# Update Slider To position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(my_slider.get()))
		
		# convert to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

		# Output time to status bar
		status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

		# Move this thing along by one second
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)



	# Output time to status bar
	#status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

	# Update slider position value to current song position
	#my_slider.config(value=int(current_time))
	
	
	# update time
	status_bar.after(1000, play_time)


#Add Song Function
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	#strip out the directory info and .mp3 extension from the song name
	song = song.replace("C:/pld/audio/", "")
	song = song.replace(".mp3", "")

	# Add song to listbox
	song_box.insert(END, song)

# Add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))	

	# Loop thru song list and replace directory info and mp3
	for song in songs:
		song = song.replace("C:/pld/audio/", "")
		song = song.replace(".mp3", "")
		# Insert into playlist
		song_box.insert(END, song)

# Play selected song
def play():
	# Set Stopped Variable To False So Song Can Play
	global stopped
	
	stopped = False
	song = song_box.get(ACTIVE)
	song = f'C:/pld/audio/{song}.mp3'
 

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Call the play_time function to get song length
	play_time()

	# Update Slider To position
	#slider_position = int(song_length)
	#my_slider.config(to=slider_position, value=0)
	
	# Get current volume
	#current_volume = pygame.mixer.music.get_volume()
	#slider_label.config(text=current_volume * 100)

	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		volume_meter.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		volume_meter.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		volume_meter.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		volume_meter.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		volume_meter.config(image=vol4)

# Stop playing current song
global stopped
stopped = False
def stop():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Stop Song From Playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

	# Clear The Status Bar
	status_bar.config(text='')

	# Set Stop Variable To True
	global stopped
	stopped = True 

	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		volume_meter.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		volume_meter.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		volume_meter.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		volume_meter.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		volume_meter.config(image=vol4)

# Play The Next Song in the playlist
def next_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)

	# Get the current song tuple number
	next_one = song_box.curselection() 
	# Add one to the current song number
	next_one = next_one[0]+1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'C:/pld/audio/{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Play Previous Song In Playlist
def previous_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Get the current song tuple number
	next_one = song_box.curselection() 
	# Add one to the current song number
	next_one = next_one[0]-1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'C:/pld/audio/{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Delete A Song
def delete_song():
	stop()
	# Delete Currently Selected Song
	song_box.delete(ANCHOR)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Delete All Songs from Playlist
def delete_all_songs():
	stop()
	# Delete All Songs
	song_box.delete(0, END)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause The Current Song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		# Pause
		pygame.mixer.music.pause()
		paused = True
	
# Create slider function
def slide(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'C:/pld/audio/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Create Volume Function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())
	
	# Get current Volume
	current_volume = pygame.mixer.music.get_volume()
	# Times by 100 to make it easier to work with
	current_volume = current_volume * 100
	#slider_label.config(text=current_volume * 100)

	# Change Volume Meter Picture
	if int(current_volume) < 1:
		volume_meter.config(image=vol0)
	elif int(current_volume) > 0 and int(current_volume) <= 25:
		volume_meter.config(image=vol1)
	elif int(current_volume) >= 25 and int(current_volume) <= 50:
		volume_meter.config(image=vol2)
	elif int(current_volume) >= 50 and int(current_volume) <= 75:
		volume_meter.config(image=vol3)
	elif int(current_volume) >= 75 and int(current_volume) <= 100:
		volume_meter.config(image=vol4)	

def my_popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)

def delay1():
    root.after(10000, root.destroy)
    
def delay2():
    root.after(30000, root.destroy)

def delay3():
    root.after(60000, root.destroy) 
    
def delay4():
    root.after(1800000, root.destroy)
    
def delay5():
    root.after(3600000, root.destroy)


def default_skin():
    master_frame.config(bg = "#374045")
    root.config(bg = "#374045")
    volume_frame.config(bg = "#374045",borderwidth=1)
    skin_frame.config(bg="#374045")
    
def orange():
    master_frame.config(bg = "#e37801")
    volume_frame.config(bg = "#e37801",borderwidth=1)
    root.config(bg = "#e37801")
    skin_frame.config(bg="#e37801")
    
def pink():
    master_frame.config(bg = "#ee8d8d")
    volume_frame.config(bg = "#ee8d8d",borderwidth=1)
    root.config(bg = "#ee8d8d")
    skin_frame.config(bg="#ee8d8d")


def red():
    master_frame.config(bg = "#bb243a")
    volume_frame.config(bg = "#bb243a",borderwidth=1)
    root.config(bg = "#bb243a")
    skin_frame.config(bg="#bb243a")
    
def violet():
    master_frame.config(bg = "#6d5382")
    volume_frame.config(bg = "#6d5382",borderwidth=1)
    root.config(bg = "#6d5382")
    skin_frame.config(bg="#6d5382")
    
    
def white():
    master_frame.config(bg = "white")
    volume_frame.config(bg = "white",borderwidth=1)
    root.config(bg = "white")
    skin_frame.config(bg="white")
    
def yellow():
    master_frame.config(bg = "#fcff81")
    volume_frame.config(bg = "#fcff81",borderwidth=1)
    root.config(bg = "#fcff81")
    skin_frame.config(bg="#fcff81")


#FRAMES ----------------------------------------------------------------------------------


#FRAME --master
master_frame = Frame(root,bg= "#374045")
master_frame.config(bg = "#374045")
master_frame.pack(pady=10,padx = 10)

# FRAME-Player Control
controls_frame = Frame(master_frame)
controls_frame.config(bg="#374045")
controls_frame.grid(row=4, column=1, padx =0,pady=0)


# FRAME -Volume Label
volume_frame = LabelFrame(master_frame, text="Volume",fg = "white", borderwidth=0, bg = "#374045")
volume_frame.config(bg = "#374045",borderwidth=1)
volume_frame.grid(row=4, column=2, padx=5,pady = 5, rowspan = 1)

# FRAME - playlist
song_box = Listbox(master_frame, bg="white", fg="black", width=34, height = 16, selectbackground="#ffe227", selectforeground="black",borderwidth= 10)
song_box.grid(row=1, column=2, pady = 0, padx = 20, columnspan = 20)

#FRAME- Logo
logo_frame = Frame(master_frame)
logo_frame.config(bg="#374045")
logo_frame.grid(row=1, column=1, padx =1,pady=0)

#FRAME- skins
skin_frame = Frame(master_frame,borderwidth = 5)
skin_frame.config(bg="#374045")
skin_frame.grid(row=1, column=0, padx =0,pady=0)







# BUTTONS --------------------------------------
#Define LOGO
logo_img = PhotoImage(file='images/logo.png')

#Define SKINS
orange_img = PhotoImage(file='images/buttons/orange.png')
pink_img = PhotoImage(file='images/buttons/pink.png')
red_img = PhotoImage(file='images/buttons/red.png')
violet_img = PhotoImage(file='images/buttons/violet.png')
white_img = PhotoImage(file='images/buttons/white.png')
yellow_img = PhotoImage(file='images/buttons/yellow.png')

# Define Player Control Button Images
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img =  PhotoImage(file='images/forward.png')
play_btn_img =  PhotoImage(file='images/play.png')
pause_btn_img =  PhotoImage(file='images/pause.png')
stop_btn_img =  PhotoImage(file='images/stop.png')

# Define Volume Control Images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file='images/volume0.png')
vol1 = PhotoImage(file='images/volume1.png')
vol2 = PhotoImage(file='images/volume2.png')
vol3 = PhotoImage(file='images/volume3.png')
vol4 = PhotoImage(file='images/volume4.png')


# Create Volume Meter
volume_meter = Label(master_frame, image=vol0)
volume_meter.grid(row=4, column=10, padx=0, columnspan = 10, rowspan = 4)


# Create Player Control Buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=3, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=3, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=3, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=3, command=lambda: pause(paused))
stop_button =  Button(controls_frame, image=stop_btn_img, borderwidth=3, command=stop)

back_button.grid(row=5, column=1, padx=2)
forward_button.grid(row=5, column=5, padx=2)
play_button.grid(row=5, column=3, padx=2)
pause_button.grid(row=5, column=2, padx=2)
stop_button.grid(row=5, column=4, padx=2)


#Create logo
logo_canvas = Button(logo_frame, image=logo_img, command=default_skin)
logo_canvas.grid(row=1, column =0, padx =1, pady=1)


#Create skin Buttons
orange_button = Button(skin_frame, image=orange_img,borderwidth=0,command=orange)
pink_button = Button(skin_frame, image=pink_img,borderwidth=0,command=pink)
red_button = Button(skin_frame, image=red_img,borderwidth=0,command=red)
violet_button = Button(skin_frame, image=violet_img,borderwidth=0,command=violet)
white_button = Button(skin_frame, image=white_img,borderwidth=0,command=white)
yellow_button = Button(skin_frame, image=yellow_img,borderwidth=0,command=yellow)

#WP ROYGBIV
orange_button.grid(row=3,column=1, padx=2)
pink_button.grid(row=1,column=1, padx=2)
red_button.grid(row=2,column=1, padx=2)
violet_button.grid(row=5,column=1, padx=2)
white_button.grid(row=0,column=1, padx=2)
yellow_button.grid(row=4,column=1, padx=2)




#MENU -----------------------------------------------------------------------------------
# Create Menu
my_menu = Menu(root, tearoff = False)
root.config(menu=my_menu)


# Main Menu
main_menu = Menu(my_menu, tearoff= 0)
submenu = Menu(main_menu, tearoff =0)
my_menu.add_cascade(label="Menu", menu=main_menu)
main_menu.add_cascade(label="Sleep Timer", menu=submenu)
submenu.add_command(label = "10 seconds", command = delay1)
submenu.add_command(label = "30 seconds", command = delay2)
submenu.add_command(label = "1 minute", command = delay3)
submenu.add_command(label = "30 minutes", command = delay4)
submenu.add_command(label = "an hour", command = delay5)


main_menu.add_cascade(label="Quit", command = quit)
	






# Create Add Song Menu 
add_song_menu = Menu(my_menu,tearoff= 0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
# Add Many Songs to playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Create Delete Song Menu
remove_song_menu = Menu(my_menu,tearoff= 0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

#Status Bar
status_bar = Label(root, text='', bd=5, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#Music Position Slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=250)
my_slider.grid(row=2, column=1, pady=0)


#Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=125)
volume_slider.pack(pady=9,padx=10)






#button 1- left click
#button 2- middle click
#button 3- right click 
root.bind("<Button-3>", my_popup)
root.mainloop()
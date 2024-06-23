from unihiker import GUI, Audio  # Import the unihiker library
import time  # Import the time library
import random #import random number generator
import threading #import threads

from pinpong.board import Board # Import the Board module from the pinpong.board package 
from pinpong.extension.unihiker import * # Import all modules from the pinpong.extension.unihiker package
 
Board().begin() # Initialize the board by selecting the board type and port number; if not specified, the program will automatically detect it

#define dog img path
dog_face = [
    "dog_faces/happy.png",
    "dog_faces/happy_eye_close.png",
    "dog_faces/normal.png",
    "dog_faces/wink.png",
    "dog_faces/tongue.png",
    "dog_faces/cool.png",
    "dog_faces/eye_heart.png",
    "dog_faces/kiss_heart.png",
    "dog_faces/sleep.png",
    "dog_faces/confuse.png"
]
 
gui = GUI()  # Instantiate a GUI object by creating an instance of the GUI class
audio = Audio()
 
img = gui.draw_image(x=0, y=0, w=240, h=320, image=dog_face[random.randrange(0, 5)])  # Display the initial background image 'light-1'
# value = gui.draw_text(x=155, y=30, text='800', font_size=18) # Display the default light value
# debug = gui.draw_text(x=40, y=30, text='N', font_size=18) # Display the debug

natural_expression = 1
sleep = 0
mic_flag = 0
acc_flag = 0

def reset_expression():
    global natural_expression, sleep, mic_flag, acc_flag
    if sleep == 0 and mic_flag == 0 and acc_flag == 0 :
        natural_expression = 1

def light_read():
    global natural_expression, sleep, mic_flag, acc_flag
    while True:
        Light = light.read() # Read the light value
#         value.config(text=Light)
        if Light < 800:
            natural_expression = 0
            sleep = 1
        else:
            reset_expression()
            sleep = 0

def mic_read():
    global natural_expression, sleep, mic_flag, acc_flag
    while True:
        Sound = audio.sound_level()
        Acc_value = accelerometer.get_strength()*100
        # value.config(text=Acc_value)
        # debug.config(text=Sound)
        if Acc_value > 110 :
            if Acc_value > 110 and Acc_value < 120 :
                natural_expression = 0
                acc_flag = 1
            if Acc_value > 120 :
                natural_expression = 0
                acc_flag = 2
        else: 
#             reset_expression()
#             acc_flag = 0
            if Sound > 50 and  sleep == 0:
                natural_expression = 0
                mic_flag = 1
#                 debug.config(text='C')
#                 change_image()
            else:
                reset_expression()
                mic_flag = 0
                acc_flag = 0
#                 debug.config(text='N')

def delay_for_acc(value):
    global natural_expression, sleep, mic_flag, acc_flag
    value = int(value/0.1)
    for i in range(value):  # range(5) generates numbers from 0 to 4
        if acc_flag == 2 :
            break 
        time.sleep(0.1)  # Delay for 1 second

def change_image():
    global natural_expression, sleep, mic_flag, acc_flag
    if sleep == 1:
        img.config(image=dog_face[8]);
    if acc_flag == 1:
        img.config(image=dog_face[random.randrange(6, 7)]);
#         time.sleep(4)  # Delay for 1 second
        delay_for_acc(4)
    if acc_flag == 2:
        img.config(image=dog_face[9]);
        time.sleep(4)  # Delay for 1 second
    if mic_flag == 1:
        img.config(image=dog_face[5]);
        time.sleep(2)  # Delay for 1 second
            
def delay(value):
    global natural_expression, sleep, mic_flag, acc_flag
    value = int(value/0.1)
    for i in range(value):  # range(5) generates numbers from 0 to 4
        if natural_expression == 0 :
            break 
        time.sleep(0.1)  # Delay for 1 second
            
def update_image():
    global natural_expression, sleep, mic_flag, acc_flag
    while True:
        if natural_expression == 1:
            img.config(image=dog_face[random.randrange(0, 5)]);
            delay(random.randrange(1, 2)/2)  # Delay for 1 second
        else:
            change_image()

# Create threads
light_read_thread = threading.Thread(target=light_read)
mic_read_thread = threading.Thread(target=mic_read)
show_image_thread = threading.Thread(target=update_image)

# Start threads
light_read_thread.start()
mic_read_thread.start()
show_image_thread.start()

# while True:  # Loop
#     img.config(image=dog_face[random.randrange(0, 5)]);
#     time.sleep(random.randrange(1, 4)/2)  # Delay for 1 second
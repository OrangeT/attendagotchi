# Attendagotchi - Attendee Tracker

from microbit import *
import music
import random

name = "@kianryan"

happiness = 5

thirst = 0
movement = 0
boredom = 0

walking = [ Image("00000:09900:99090:90090:09900"),
           Image("00000:09900:90990:90090:09900"),
           Image("00000:00990:09099:09009:00990"),
           Image("00000:00990:09909:09009:00990")]

last_gx = accelerometer.get_x()
move_count = 0

music_played = False

last_time = running_time()

def increase_happiness():
    global happiness

    if happiness < 10:
        happiness = happiness + 1
        display.show(Image.HAPPY)
        music.play(music.DADADADUM)

def decrease_happiness():
    global happiness
    
    if happiness > 0:
        happiness = happiness - 1
        display.show(Image.SAD)
        music.play(music.WAWAWAWAA)

def show_introduction():
    global happiness, music_played

    #display.scroll("Hello, I'm " + name + ".")

    for _ in range(2):
        display.show(walking, loop=False, delay=500)
    if happiness > 3:
        display.show(Image.HAPPY)
        if not music_played:
            music.play(music.POWER_UP)
            music_played = True
        else:
            sleep(1000)

    elif happiness > 0:
        display.show(Image.CONFUSED)
        sleep(1000)

    else:
        display.show(Image.SAD)
        if not music_played:
            music.play(music.POWER_DOWN)
            music_played = True
        else:
            sleep(1000)

# Play the traditional game of chance
def play_game():
    score = 0
    for x in range(0, 5):

        # Set result
        actual = random.choice(["A", "B"])

        # Guess
        display.show(Image.DIAMOND)
        guess = None
        while(guess == None):
            if button_a.is_pressed():
                guess = "A" 
            elif button_b.is_pressed():
                guess = "B"

        # Show
        if actual == "A":
            display.show(Image.ARROW_W)
        else:
            display.show(Image.ARROW_E)

        sleep(1000)

        # Judge
        if guess == actual:
            score = score + 1
            display.show(Image.HAPPY)
            music.play(music.DADADADUM)
        else:
            display.show(Image.SAD)
            music.play(music.WAWAWAWAA)

    return score > 2

def update_counters():
    global thirst, move_count, boredom, happiness, last_time

    # Update counters by seconds since last
    # read.

    curr_time = running_time()
    interval_time = int((curr_time - last_time) / 1000)
    last_time = curr_time


    # Thirst
    thirst = thirst + interval_time

    # Movement
    curr_gx = accelerometer.get_x()
    if abs(curr_gx - last_gx) > 100:
        move_count = move_count + interval_time
    else:
        move_count = 0

    # Boredom
    boredom = boredom + interval_time

def update_happiness():
    global thirst, movement, boredom, happiness


    # Thirst
    if thirst > 900: # 15 minutes
        decrease_happiness()
        thirst = 0

    # Movement
    if move_count > 30:
        movement = 0
        increase_happiness()
    else:
        movement = movement + 1

    if movement > 3600:
        decrease_happiness()
        movement = 0

    # Boredom
    if boredom > 3600:
        happiness = happiness - 1
        boredom = 0

def read_buttons():
    global thirst, boredom

    # Left Button - Drink
    if button_a.was_pressed():
        display.show(Image.PACMAN)
        sleep(1000)

        if (thirst > 100):
            increase_happiness()

        if (thirst < 20):
            decrease_happiness()

        thirst = 0

    # Right Button - Game
    if button_b.was_pressed():
        boredom = 0

        if (play_game() == True):
            increase_happiness()
        else:
            decrease_happiness()

def print_debug():
    print("Happiness:" + str(happiness) + 
            " Thirst:" + str(thirst) + 
            " Movement:" + str(movement) + 
            " Boredom:" + str(boredom))

while True:
    show_introduction()
    print_debug()
    update_counters()
    update_happiness()
    read_buttons()

from PIL import ImageGrab
from pynput.mouse import Button, Controller
import pyautogui
import time
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
import time

def start_browser():
    firefoxProfile = FirefoxProfile()
    firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','true')
    firefoxProfile.set_preference("plugin.state.flash", 2)
    b = webdriver.Firefox(firefoxProfile)

    b.get("https://www.tanktrouble.com/")

pyautogui.FAILSAFE = True
game_location = (620, 170, 1325, 570)

keys_x = ['left', 'right']
keys_y = ['down',]

# Screenshot filename

screenshot_filename = 'game.png'

# players icon filename
laika_icon = 'laika.png'
red_icon = 'red.png'
redpoint_icon = 'redpoint.png'

# bal location
ball_icon = 'ball.png'

gun_type = 'gun'
ammo = 3

def start_game():
    button_location_btn =756, 521
    mouse = Controller()
    screenWidth, screenHeight = pyautogui.size()
    time.sleep(1)
    pyautogui.moveTo(button_location_btn)
    time.sleep(3)
    mouse.click(Button.left, 2)
    pyautogui.press("m")



fire = [True, False]
def get_screen():
    return ImageGrab.grab(game_location)
img = None
def locate_image_location(template, image, out_file=True):
    img = cv2.imread(template, 0)
    img2 = cv2.imread(template, 0)
    img2 = img.copy()
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]

    img = img2.copy()
    method = cv2.TM_CCOEFF

    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    location = (top_left, bottom_right, 255, 2)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    if out_file:
        cv2.imwrite('game.png', img)

    return location


def get_laika_location():
    return locate_image_location(screenshot_filename, laika_icon)


def get_my_location():
    return locate_image_location(screenshot_filename, red_icon)

def get_my_pointing():
    return locate_image_location(screenshot_filename, redpoint_icon)


def get_balls_location():
    return locate_image_location(screenshot_filename, ball_icon)


def play_game():
    while True:
        get_screen().save('game.png')
        # get players location
        laika_location = get_laika_location()
        red_location = get_my_location()

        # check for balls
        balls = get_balls_location()

        # where am I pontin to ? (orientation)
        my_pointing = get_my_pointing()

        # Am I pointing to a wall ?

        # is there a ball nearme ? hell run away !!
        print("me : {} orientation: {}  laika: {} ball : {}".format(red_location, my_pointing, laika_location, balls))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Laiak',(laika_location[0][0], laika_location[1][0]), font, 4,(255,255,255),2,cv2.LINE_AA)
        kx = keys_x[random.randint(0, 1)]
        ky = keys_y[random.randint(0, 0)]
        print("pressing : {} and {}".format(kx, ky))
        pyautogui.keyDown(kx)
        pyautogui.keyDown(ky)
        time.sleep(.001)
        pyautogui.keyUp(kx)
        pyautogui.keyUp(ky)
        if fire[random.randint(0,1)]:
            print("FIRE!!!!!!")
            pyautogui.keyDown('m')
            pyautogui.keyUp('m')

play_game()

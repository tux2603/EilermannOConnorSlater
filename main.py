import os
import pyautogui as p
import Xlib
import Xlib.display

from time import sleep, time
from PIL import Image
from pynput.mouse import Button, Controller
from random import random
from threading import Thread


def openWindow():
    global window, WIDTH, HEIGHT, display
    os.system('clear')

    # Open the browser
    os.system('firefox "https://agar.io" -new-window -private &')
    sleep(2)

    # Resize the browser
    display = Xlib.display.Display()
    root = display.screen().root

    # Get the x windows ID of the browser
    windowID = root.get_full_property(display.intern_atom(
        '_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
    window = display.create_resource_object('window', windowID)
    window.configure(width=WIDTH, height=HEIGHT)
    display.sync()


# def getWindowPosition():
#     id = Xlib.display.Window
#     parent = id.query_tree().parent
#     return (parent.X, parent.Y)


def login():
    # Find and click the play button
    p.moveTo(1, 1)
    while 1:
        loc = p.locateOnScreen(
            'ReferenceImages/playButton.png', confidence=0.9)
        if loc is not None:
            break
    p.moveTo(x=loc.left + 0.5 * loc.width, y=loc.top + 0.5 * loc.height)

    # Type in the name and startt
    p.moveRel(0, -20)
    p.click()
    sleep(0.5 + random())
    p.hotkey('ctrl', 'a')
    sleep(0.5 + random())
    p.typewrite('iRobot', interval=0.5 + random())
    sleep(0.76 + random())
    p.press('enter')
    if SPEAK:
        os.system('espeak -p00 -s80 "I wish to eat you" &')


def deathSound():
    if SPEAK:
        os.system('espeak -p00 "oh no... I died!" &')


def captchaSound():
    if SPEAK:
        os.system('espeak -p00 "Curses. Foiled again. I hate bloody captchas" &')


class DeathChecker(Thread):
    def __init__(self):
        super().__init__()
        self.isDead = False
        self.isDetected = False

    def run(self):
        while 1:
            loc = p.locateOnScreen('ReferenceImages/continueButton.png', confidence=0.9)
            if loc is not None:
                self.isDead = True
                break
            loc = p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9)
            if loc is not None:
                self.isDetected = True


if __name__ == '__main__':
    WIDTH, HEIGHT = 600, 400
    display = None
    SPEAK = True
    window = None
    dead = False

    openWindow()
    login()

    # Starting death checking to kill program
    checker = DeathChecker()
    checker.start()

    mouse = Controller()

    # Game Loop
    while not checker.isDead:
        if checker.isDetected:
            # Ask to solve captcha
            captchaSound()
            window.configure(width=1500, height=900)
            display.sync()
            sleep(1)

            # Wait for captcha to be solved
            while 1:
                if p.locateOnScreen('ReferenceImages/captchaSolve.png', confidence=0.9) is None and p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9) is None:
                    sleep(1)
                    if p.locateOnScreen('ReferenceImages/captcha.png', confidence=0.9) is None:
                        break
            checker.isDetected = False
            window.configure(width=WIDTH, height=HEIGHT)
            display.sync()

        t0 = time()
        mouse.position = (random() * 500, random() * 500)
        sleep(1 / 144)
        print('{} FPS'.format(round(1 / (time() - t0), 3)))

    deathSound()
    print('we ded')
    print(vars(window.get_image(0, 0, 10, 10, Xlib.X.ZPixmap, 0xffffffff)), type(window.get_image(0, 0, WIDTH, HEIGHT, Xlib.X.ZPixmap, 0xffffffff)))
    raw = window.get_image(0, 0, WIDTH, HEIGHT, Xlib.X.ZPixmap, 0xffffffff)
    image = Image.frombytes('RGB', (WIDTH, HEIGHT), raw._data['data'], 'raw', 'BGRX')
    image.show()

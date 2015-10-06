#!/usr/bin/python

'''
    @author Alwin Chan <alwin@d2u.us>
    @url    https://github.com/alwinchan/cocloolector
    @version 1.0
'''

import os
import random
import unittest
import cv2
import re
import numpy as np
import sys, getopt
import pytesseract
from PIL import Image
from time import sleep

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from matplotlib import pyplot as plt

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Screen:
    pass

screen = Screen()

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"p:d:")

for o, a in myopts:
    if o == '-p':
        port=a
    elif o == '-d':
        device=a
    else:
        print("Usage: %s -p <port> -d <deviceID>" % sys.argv[0])

print "Device: %s" % device
print "Port: %s" % port
# sys.exit(0)

def get_position(desc, needle, uniquePoints=True, threshold=0.75):
    global screen
    print "\r[%s] %s" % (port, desc[0])
    points = []
    needle_img = cv2.imread(needle, 0)
    w, h = needle_img.shape[::-1]
    res = cv2.matchTemplate(screen.img_gray, needle_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        x = pt[0]+8
        y = pt[1]+8         
        # print '[%s] Found %s: %d,%d\r' % (port, desc[1], x, y)
        skip=False
        for ex in points:
            ex_x = ex[0]
            ex_y = ex[1]
            if ex_x - x > 5 or ex_x - x > -5 or ex_y - y > 5 or ex_y - y > -5:
                skip=True
                break

        if uniquePoints is False:
            skip=False

        if skip is False:
            print '[%s] Found %s\r' % (port, desc[1])
            # print '[%s] Found %s: %d,%d\r' % (port, desc[1], x, y)
            cv2.rectangle(screen.img_rgb, pt, (x-8 + w, y-8 + h), (0,255,0), 1)
            points.append( [x, y] )
            cv2.circle(screen.img_rgb, (x, y), 2, (255,0,0), -1)
    return points

def take_screenshot(self):
    global screen
    directory = '%s/' % os.getcwd()
    screen.file_name = 'downloads/screenshot.%s.png' % port
    self.driver.save_screenshot(directory + screen.file_name)

    resolution = cv2.imread(screen.file_name, 0)
    w, h = resolution.shape[::-1]

    if w < h:
        im1 = Image.open(screen.file_name)
        im2 = im1.rotate(90)
        im2.save(screen.file_name)

    screen.img_rgb = cv2.imread(screen.file_name)
    screen.img_gray = cv2.cvtColor(screen.img_rgb, cv2.COLOR_BGR2GRAY)

    sleep(1)

    return screen

def has_text(text):
    global screen
    image = Image.open(screen.file_name)
    textFromImage = pytesseract.image_to_string(image, lang='eng')
    a = re.search(text, textFromImage)
    if a:
        print a.group(0)
        return True
    return False

def actionTap(self, obj, screenshotAfterTap=True):
    TouchAction(self.driver).press(x=obj[0][0], y=obj[0][1]).release().perform()
    sleep(1)
    if screenshotAfterTap:
        take_screenshot(self)
    return

def actionTapXY(self, pointX, pointY):
    TouchAction(self.driver).press(x=pointX, y=pointY).release().perform()
    sleep(1)
    return

def ifTextWaitThenTap(self, text, wait, button):
    print "[%s] Check if screen has text: %s" % (port, text)
    if has_text(text):
        sleep(wait)
        button = get_position(['Try to locate button', 'Button'], button)
        if len(button) > 0:
            actionTap(self, button)
    return

class ComplexAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.3'
        desired_caps['deviceName'] = device
        desired_caps['androidPackage'] = 'com.supercell.clashofclans'
        desired_caps['appActivity'] = 'GameApp'
        # desired_caps['autoLaunch'] = 'false'
        desired_caps['noReset'] = 'true'
        # desired_caps['app'] = PATH(
        #     'com.supercell.clashofclans-1.apk'
        # )
        # super(ComplexAndroidTests, self).setUp()

        self.driver = webdriver.Remote("http://localhost:%s/wd/hub" % port, desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_tap_nothing(self):
        global screen
        skipScreenshot = False
        activity = self.driver.current_activity
        print "\r[%s] Current Activity: %s\r" % (port, activity)
        # assertEquals('.GameApp', activity)

        loaded=False
        while loaded is False:
            take_screenshot(self)
            attack = get_position(['Check for status...', 'Game Loaded'], 'res/loaded.png')
            if len(attack) > 0:
                loaded=True
                break
            else:
                sleep(2)

        while True:
            take_screenshot(self)

            ifTextWaitThenTap(self, 'Another device is connecting to this village', (60*10), 'res/btn_reload.png')

            ifTextWaitThenTap(self, 'You have been playing for too long', (60*5), 'res/btn_reload.png')

            ifTextWaitThenTap(self, 'Unable to connect with the server', 60, 'res/btn_try-again.png')

            if vars().has_key('wasAttacked') is False:
                wasAttacked = get_position(['Checking if village was attacked?', 'was attacked'], 'res/village-was-attacked.png')

                if len(wasAttacked) > 0:
                    okay = get_position(['Okay to proceed', 'okay'], 'res/btn_okay.png')
                    if len(okay) > 0:
                        actionTap(self, okay, skipScreenshot)

            # zoom out
            print "\r[%s] Zooming out" % port
            finger1 = TouchAction().press(x=100, y=200).move_to(x=200, y=300).release()
            finger2 = TouchAction().press(x=600, y=700).move_to(x=-100, y=-100).release()
            ma = MultiAction(self.driver)
            ma.add(finger1, finger2)
            ma.perform()
            sleep(1)

            # capture screenshot
            take_screenshot(self)

            armyOverview = get_position(['Checking Army Overview', 'Army Overview'], 'res/btn_train.png')

            if len(armyOverview) > 0:
                actionTap(self, armyOverview)

                requestAvail = get_position(['Checking if Request available?', 'Request Available'], 'res/btn_request-available.png')

                if len(requestAvail) > 0:
                    actionTap(self, requestAvail)

                    requestTroop = get_position(['Request for troops now!', 'Send Button'], 'res/btn_send.png')

                    if len(requestTroop) > 0:
                        actionTap(self, requestTroop)
                        print "\r[%s] Troops Request sent!" % port

                closeButton = get_position(['Close Army Overview', 'Close Button'], 'res/btn_close.png')
                if len(closeButton) > 0:
                    actionTap(self, closeButton)

            slideMenu = get_position(['Open the left slide menu', 'Slide Menu'], 'res/btn_slide-open.png')

            if len(slideMenu) > 0:
                actionTap(self, slideMenu)

                donateButton = get_position(['Checking if anyone request for troops', 'Donate Button'], 'res/btn_donate.png')

                if len(donateButton) > 0:

                    for donate in donateButton:
                        x = donate[0]
                        y = donate[1]

                        actionTapXY(self, donate[0], donate[1])
                        take_screenshot(self)

                        archerAvailable = get_position(['Try to donate some archer', 'Archer'], 'res/unit_archer.png')
                        if len(archerAvailable) > 0:
                            count = 0
                            while count <= 10:
                                actionTap(self, archerAvailable, skipScreenshot)
                                count += 1

                        take_screenshot(self)

                        closeDonateBox = get_position(['Close the donate box', 'Close Donate Box'], 'res/btn_close.png')
                        if len(closeDonateBox) > 0:
                            actionTap(self, closeDonateBox)

                closeSlideMenu = get_position(['Close the left slide menu', 'Close Slide Menu'], 'res/btn_slide-close.png')

                if len(closeSlideMenu) > 0:
                    actionTap(self, closeSlideMenu)

            sleep(1)

            print "\r[%s] Looking for l00ts :D" % port

            loots = []
            elixir = get_position(['Looking for Elixir', 'Elixir'], 'res/elixir.png')
            if len(elixir) > 0:
                loots = loots + elixir

            darkElixir = get_position(['Looking for Dark Elixir', 'Dark Elixir'], 'res/dark-elixir.png')
            if len(darkElixir) > 0:
                loots = loots + darkElixir

            coin = get_position(['Looking for Coin', 'Coin'], 'res/coin.png')
            if len(coin) > 0:
                loots = loots + coin

            # Connection error - Unable to connect with the server. Check your internet connection and try again. [Try again]
            # Connection lost - Another device is connecting to this village. [Reload]
            # Take a break - You have been playing for too long and your villagers need to rest for a few minutes. [Reload]

            cv2.imwrite('downloads/res.%s.png' % port, screen.img_rgb)
            sleep(1)

            if len(loots) > 0:
                for point in loots:
                    actionTapXY(self, point[0], point[1])
                    actionTapXY(self, 900, 220)
                    actionTapXY(self, 1075, 45)

            sleep(random.randint(1,10))

        return

        # so you can see it
        sleep(10)

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(ComplexAndroidTests)
        unittest.TextTestRunner(verbosity=9).run(suite)
    except (KeyboardInterrupt, SystemExit):
        print "\rExiting...                              \r"

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
import numpy as np
import sys, getopt
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

        activity = self.driver.current_activity
        print "\r[%s] Current Activity: %s" % (port, activity)
        # assertEquals('.GameApp', activity)

        sleep(30)

        # zoom out
        print "\r[%s] Zooming out" % port
        finger1 = TouchAction().press(x=100, y=200).move_to(x=200, y=300).release()
        finger2 = TouchAction().press(x=600, y=700).move_to(x=-100, y=-100).release()
        ma = MultiAction(self.driver)
        ma.add(finger1, finger2)
        ma.perform()

        sleep(1)
        
        while True:    
            points = []

            print "\r[%s] Looking for l00ts :D" % port
            directory = '%s/' % os.getcwd()
            file_name = 'downloads/screenshot.%s.png' % port
            self.driver.save_screenshot(directory + file_name)

            resolution = cv2.imread(file_name, 0)
            w, h = resolution.shape[::-1]

            if w == 720 and h == 1280
                im1 = Image.open(file_name)
                im2 = im1.rotate(90)
                im2.save(file_name)

            sleep(2)

            img_rgb = cv2.imread(file_name)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            elixir = cv2.imread('res/elixir.png',0)
            w, h = elixir.shape[::-1]
            res = cv2.matchTemplate(img_gray, elixir, cv2.TM_CCOEFF_NORMED)
            threshold = 0.75
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                print '[%s] Found Elixir: %d,%d\r' % (port, pt[0], pt[1])
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 1)
                points.append( [pt[0]+8, pt[1]+8] )
                cv2.circle(img_rgb,(pt[0]+8, pt[1]+8), 2, (255,0,0), -1)
                # break

            darkElixir = cv2.imread('res/dark-elixir.png',0)
            w, h = darkElixir.shape[::-1]
            res = cv2.matchTemplate(img_gray, darkElixir, cv2.TM_CCOEFF_NORMED)
            threshold = 0.75
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                print '[%s] Found Dark Elixir: %d,%d\r' % (port, pt[0], pt[1])
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,0,0), 1)
                points.append( [pt[0]+8, pt[1]+8] )
                cv2.circle(img_rgb,(pt[0]+8, pt[1]+8), 2, (255,0,0), -1)
                # break

            coin = cv2.imread('res/coin.png',0)
            w, h = coin.shape[::-1]
            res = cv2.matchTemplate(img_gray,coin,cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                print '[%s] Found Coin: %d,%d\r' % (port, pt[0], pt[1])
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                points.append( [pt[0]+8, pt[1]+8] )
                cv2.circle(img_rgb,(pt[0]+8, pt[1]+8), 2, (255,0,0), -1)
                # break

            cv2.imwrite('downloads/res.%s.png' % port, img_rgb)

        # while len(points) > 0:
            sleep(2)

            # random_index = random.randint(0, len(points)-1)
            # point = points[random_index]

            if len(points) > 0:
                for point in points:

                    TouchAction(self.driver).press(x=point[0], y=point[1]).release().perform()
                    sleep(1)
                    TouchAction(self.driver).press(x=900, y=220).release().perform()
                    sleep(1)
                    TouchAction(self.driver).press(x=1075, y=45).release().perform()
                    sleep(1)

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

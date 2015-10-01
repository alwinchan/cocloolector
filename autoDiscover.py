#!/usr/bin/python

'''
    @author Alwin Chan <alwin@d2u.us>
    @url    https://github.com/alwinchan/cocloolector
    @version 1.0
'''

import subprocess
import sys
import os
from time import sleep

p = subprocess.Popen('bin/adb devices', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

appiumPort=4723
appiumBPort=2251

def cmd(command, stdout=False):
  command = "%s" % (command)
  proc=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  if stdout:
	return proc.stdout.read()
  else:
	return proc.communicate()[0]
  return

for line in p.stdout.readlines():
	if "device\n" in line:
		line = line.strip('\n')
		line = line.strip('\t')
		lines = line.split("device")
		
		device = lines[0].strip('\t')

		# print "appium -p %s -bp %s -U %s" % (appiumPort, appiumBPort, device)
		subprocess.Popen("appium -p %s -bp %s -U %s > appium-%s.log" % (appiumPort, appiumBPort, device, appiumPort), shell=True, stderr=subprocess.STDOUT)
		
		sleep(5)

		subprocess.Popen("python cocloolector.py -p %s -d %s &" % (appiumPort, device), shell=True, stderr=subprocess.STDOUT)

		appiumPort += 10
		appiumBPort += 10

retval = p.wait()
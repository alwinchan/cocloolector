#!/bin/sh

# @author 	Alwin Chan <alwin@d2u.us>
# @url 		https://github.com/alwinchan/cocloolector
# @version	1.0

set -e

tput=$(which tput)
if [ -n "$tput" ]; then
    ncolors=$($tput colors)
fi
if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
  RED="$(tput setaf 1)"
  GREEN="$(tput setaf 2)"
  YELLOW="$(tput setaf 3)"
  BLUE="$(tput setaf 4)"
  BOLD="$(tput bold)"
  NORMAL="$(tput sgr0)"
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  BOLD=""
  NORMAL=""
fi

if [[ "which brew" = *not found* ]]; then
	echo
	read -n 1 -p "${RED} You must have ${GREEN}brew${RED} installed first. Install now? [y/n]" yes
	echo
	if [ "$yes" == "Y" ]; then
		ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	else
		echo "${BLUE}Try again after you have installed brew. Bye!${NORMAL}"
	fi
fi

if [[ "which brew" = *not found* ]]; then
	brew install python
else
	python -V
fi

if [[ "pkg-config --modversion opencv" = *not found* ]]; then
	brew tap homebrew/science
	brew install opencv
	echo "OpenCV for Python: " -n
	pkg-config --modversion opencv
fi

if [[ "pip -V" = *not found* ]]; then
	brew install pip
else
	pip -V
fi


if [[ "node -v" = *not found* ]]; then
	brew install node
else
	echo "node " -n
	node -v
fi

if [[ "appium -v" = *not found* ]]; then
	npm install -g appium
else
	echo "appium " -n
	appium -v
fi

if [[ "which wd" = *not found* ]]; then
	npm install -g wd
fi

pip install Pillow
pip install matplotlib
pip install numpy
pip install Appium-Python-Client

git clone https://github.com/alwinchan/cocloolector.git
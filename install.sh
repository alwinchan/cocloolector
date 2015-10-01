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

if [ ! -n "$(which brew)" ]; then
	echo
	read -n 1 -p "${RED} You must have ${GREEN}brew${RED} installed first. Install now? [y/n]" yes
	echo
	if [ "$yes" == "Y" ]; then
		ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	else
		echo "${BLUE}Try again after you have installed brew. Bye!${NORMAL}"
	fi
fi

echo
echo "${YELLOW}Checking dependancies...${NORMAL}"

if [ ! -n "$(which python)" ]; then
	brew install python
else
	python -V
fi

if [ ! -n "$(pkg-config --modversion opencv)" ]; then
	brew tap homebrew/science
	brew install opencv
	echo -n "OpenCV for Python: "
	pkg-config --modversion opencv
fi

if [ ! -n "$(pip -V)" ]; then
	brew install pip
else
	pip -V
fi


if [ ! -n "$(node -v)" ]; then
	brew install node
else
	echo -n "node "
	node -v
fi

if [ ! -n "$(appium -v)" ]; then
	npm install -g appium
else
	echo -n "appium "
	appium -v
fi

if [ ! -n "$(which wd)" ]; then
	npm install -g wd
fi

pip install Pillow
pip install matplotlib
pip install numpy
pip install Appium-Python-Client

git clone https://github.com/alwinchan/cocloolector.git

echo
echo "${GREEN}Successfully install into ${BOLD}cocloolector${NORMAL}"
echo
echo "${YELLOW}Now run:"
echo "${YELLOW}cd cocloolector && python autoDiscover.py"
echo
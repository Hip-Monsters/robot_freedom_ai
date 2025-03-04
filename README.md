#  RobotFreedomAI 

The official RobotFreedom.com robotic control library.


## What's new

This is a test release and not intended to be used for any purpose other than testing. 

There is still tons of work to do. 
 

## Getting Started

When designing Robot Freedom AI, our educational presentation on robotics, the HipMonster's team wanted to make robotics and artificial intelligence (AI) approachable to a mass audience in hopes of inspiring the creators within all of us. To achieve this, the core principles for our AIis that each robots should have distinct personalities, emotions, curiosity and be first and foremost pieces of art.

Given these principles, the foundation of our artificial intelligence framework (show above) is based on Stimulus Organism Response (S-O-R) Theory. S-O-R theory is a psychological framework that enables researchers to explore how stimuli (such as a bell) can impact an organism's responses, (a dog salivating). Like Pavlov's dog salivating at the sound of a bell, our robots learn and adapt as they experience outside stimuli and are always eager for more. The robot's AI is driven by five personality traits that govern how they interpret and respond to stimuli. Below is how a signal from a sensor (stimuli) flows through our AI (organism) and results in an action (response).

Central to the robot's stimuli exploration is a sensor array of ten sensors ranging from sound to touch. When a robot receives a stimulus, it first processes the information based on its preset personality, then uses past experiences to choose a response based on its personality. Below is a color key to the robot's sensor display panel.

These experiences are weighted based on the outcome of the robot's actions allowing the robot to adapt responses to new stimuli. The robots can move, change visual effects, or talk using a chatbot. Below is the full software stack used in our robots.

## Installation

First, download this repro and unzip it on your Desktop or projects folder. Then, open a terminal and navigate to robot_freedom_ai.

Note: We perfer to not install robot_freedon_ai as a package because this project is primarily a teaching tool not production code. We want people to experiement and change the code on demand and a package installations make this difficult.  

The set up is slight different dependig on whether you are using OSX, Windows or Linux. The code will run on degraded mode on most platforms but will only be fully functional on a RaspberryPi. 

First, if you do not have Python3 and Pip installed please do before you begin.
HTTP;// install ptheyon

### RaspberryPI

python3 -m venv .venv
source .venv/bin/activate

sudo apt install memcached libmemcached-tools -y
sudo apt install -y libportaudio2   
sudo apt install -y python3-picamera2
sudo apt-get install git libpcap-dev
sudo apt install -y python3-libcamera python3-kms++ libcap-dev
sudo apt install espeak-ng
sudo apt-get install portaudio19-dev python-pyaudio python3-pyaudio
sudo apt install python3-pyaudio

pip install -r requirements.txt

We have had mixed luck with not installing sound and video related packages in a Python venv. If you use the venv and it does not work then you can install all the packages into the system Python using the --break-system-packages command. Most of our robots have used this method and we have never seen any adverse effects.

pip install vosk --break-system-packages   
pip install piper-tts --break-system-packages
 


### OSX
 

python3 -m venv .venv
source .venv/bin/activate

sudo apt install memcached libmemcached-tools -y
brew install portaudio
 
pip install -r requirements.osx.txt


### Windows 10

Install memcache
https://www.geeksforgeeks.org/how-to-install-memcached-on-windows/


python3 -m venv .venv
source .venv/bin/activate
  
 
pip install -r requirements.win.txt


###

python -m  ollama pull allenporter/xlam:1b 
python -c "from vosk import Model; Model(lang='en-us')"


## Networked 


## Protocols

### Monitor

### Listen

### Script
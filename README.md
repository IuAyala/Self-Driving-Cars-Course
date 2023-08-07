# Machine Learning & Self-Driving Cars: Bootcamp with Python Exercises

This repository stores code for the course: Machine Learning & Self-Driving Cars: Bootcamp with Python Exercises - [Get Lectures](https://gradientinsight.com/learning/)

# Index

- [Course Sections](#course-sections)
- [Installation](#installation)
  - [Linux](#linux)
  - [Windows](#windows)
- [Usage](#usage)
- [Contact](#contact)

# Course Sections

- Python: code used for lectures (it's recommended to start from scratch)
- Computer Vision: using the simulator Webots, we will make a car follow the road line
- Machine Learning (Road Sign Classification): we will use Machine Learning to classify road signs (i.e. the model will be able to tell if the image contains a stop sign, speed limit sign, ...)
- Collision Avoidance: Using a Lidar we will make make our car drive without crashing
- Deep Learning (Behavioural Clonning): Using the power of Deep Neural Networks we will make the car drive like ourselves!

# Installation

- Install Python
- Install Visual Studio Code
- Install Webots
- Install Python libraries (can be found in 0_install/requirements.txt)
- Add Envrionment Variables (PYTHONPATH, PYTHONDECODING, ...)
  **NOTE:** There are OS specific instructions (Windows & Linux)

## Linux

### Install Webots

Install on Debian-based systems (i.e. Ubuntu), open a terminal and paste the following commands (shortcut: Ctrl+Alt+T), then paste:

```
wget -qO- https://cyberbotics.com/Cyberbotics.asc | sudo apt-key add - # Add the key with the command
sudo apt-add-repository 'deb https://cyberbotics.com/debian/ binary-amd64/' # Add the repository
sudo apt-get update
sudo apt-get install webots # install Webots
```

Alternative you can install it through the snap store:

```
sudo apt-get install snapd
sudo snap install webots
```

Official documentation - [link](https://cyberbotics.com/doc/guide/installation-procedure#installation-on-linux)

### Automated installation of the rest (Python, Visual Studio Code, Python Libraries, Environment Variables) - Linux

You can install everything necessary in _Linux_ by executing the following on a terminal.

```
cd ~/Code/Self-Driving-Cars-Course/0_install # set the right path, this will work with the default path
./install_linux.sh
```

Note: This method should work for: Ubuntu, Fedora, Arch-based distros

### Manual installation of the rest (Python, Visual Studio Code, Python Libraries, Environment Variables) - Linux

Install:

- Python, execute `sudo apt-get install python3`
- Visual Studio Code
  - Download it [here](https://code.visualstudio.com/download) in Ubuntu download the ".deb" version
  - If it gets stored in the Downloads folder install it with `sudo apt-get install ~/Downloads/code_*.deb`

To set up the environment variables, open a terminal and run the following commands:

```
echo "export WEBOTS_HOME=/usr/local/webots" >> ~/.bashrc
echo "WEBOTS_PYTHON=${WEBOTS_HOME}/lib/controller/python" >> ~/.bashrc
echo "export PYTHONPATH=${PYTHONPATH:+${PYTHONPATH}:}${WEBOTS_PYTHON}" >> ~/.bashrc
echo "export PYTHONIOENCODING=UTF-8" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}${WEBOTS_HOME}/lib/controller" >> ~/.bashrc
```

Validate intallation, run the following command:

```
PYTHONPATH=$(echo $PYTHONPATH | tr ':' '\n')
last_element=$(tail -n 1 <<< "$PYTHONPATH")
ls ${last_element}/controller/robot.py
```

Should output something like:
`/usr/local/webots/lib/controller/python/controller/robot.py`
Otherwise your Python won't have access to the Webots library. If you get something like `ls: cannot acces...` then you need to make sure that the paths you entered are present in your machine (feel free to contact the repo owner if you are having issues with that).

Official documentation - [link](https://cyberbotics.com/doc/guide/using-your-ide?tab-language=python&tab-os=linux#pycharm)

## Windows

### Install Webots - Windows

- Download the "webots-R2022a_setup.exe" installation file from their [website](https://cyberbotics.com/)
- Double click on this file
- Follow the installation instructions

Official documentation - [link](https://cyberbotics.com/doc/guide/installation-procedure#installation-on-windows)

### Manual Installation - Windows

Install:

- [Python](https://www.python.org/downloads/)
  - Make sure you tick "Add Python 3.X to PATH"
- [Visual Studio Code](https://code.visualstudio.com/download)

Install the required Python libraries:

- Open "git bash", execute:
  ```
  cd ~/Code/Self-Driving-Cars-Course/0_installation
  pip3 install -r requirements.txt
  ```

Set the required environment variables

- Click the "Windows Key" and write "Edit the system environment variables"
- Create variable “WEBOTS_HOME” with content “C:\Program Files\Webots”
- Create variable “PYTHONPATH” with content “%WEBOTS_HOME%/lib/controller/python”
  - Note: Order version of Webots used to have a specific python folder for each subversion i.e. python39
- Add to “PATH”
  - “%WEBOTS_HOME%\lib\controller”
  - “%WEBOTS_HOME%\msys64\mingw64\bin”
  - “%WEBOTS_HOME%\msys64\mingw64\bin\cpp”
- Create variable “PYTHONIOENCODING” with content “UTF-8”

Official documentation - [link](https://cyberbotics.com/doc/guide/using-your-ide?tab-language=python&tab-os=windows#pycharm)

# Usage

Each section has a set of files, the ones that have leading numbers (i.e. 1*, 2*, ...) are the ones that should be executed, in the order marked by the leading numbers.

Some of them require some preparation (i.e. run Webots simulator, download dataset):

- **1_python_tutorial**: doesn't require anything
- **2_computer_vision**: requires Webots (words/city.wbt)
- **3_collision_avoidance**: requires Webots (worlds/city_with_borders.wbt)
- **4_machine_learning**: requires to download the [dataset](https://www.kaggle.com/andrewmvd/road-sign-detection) and save it to the "4_machine_learning/original_dataset" folder, add the folders "images/" and "annotations/" inside the "original_datatset" folder
- **5_behavioural_cloning**: requires Webots (words/city.wbt)

NOTE: When it requires any Webots world (.wbt) you can open it in Webots by clicking "File-->Open World".

# Contact

If you have any problem with the code the best way to contact me is Udemy Q&A section. Leave your question there and I'll answer as soon as possible!

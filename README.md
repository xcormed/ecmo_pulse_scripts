# Pulse setup

The pulse repository requires the presence of three main applications on the path in order to build: CMAKE, Java,and Python

CMAKE: You have the option to download and install cmake from the website: this will also give you access to the cmake GUI (I haven't found the GUI to work very well with this) Besides you will need to manually set the path.

You can also install cmake using terminal commands: 'pip install cmake' should install cmake on the computer and it should be available on the path.
JAVA: The Pulse website recommends a download from Amazon. It is possible that you are already running Java on your computer, but it may not have all the requirements. I would still recommend using amazon coretto, and as long as

PYTHON: As of August 2022, Pulse would not build correctly with Python 3.10. There are no apparent errors and the sourse code builds to completion but you will get a PyPulse.so file instead of the required PyPulse-cypthon-'pythonversion'-darwin.so. In python 3.9, this would be PyPulse-cypthon-'39'-darwin.so
Follow directions on the Pulse website to download the source code and build: [Pull and build]([https://gitlab.kitware.com/physiology/engine#building])

After a successful build, Ensure ability to run HowTo examples: cd into the install/bin folder and run: python3 ~/Pulse/engine/src/python/howto/HoWTo_example

The next step involves setting up Pycharm. Download Pycharm from https://www.jetbrains.com/pycharm/. If you intend to use Google cloud Platform, make sure to download Pycharm Pro and activate an account.
Follow these steps to set up the Pulse project in Pycharm: https://gitlab.kitware.com/physiology/engine/-/wikis/Using-Pycharm


# ecmo_pulse_scripts

In order to generate graphs, you first need to run all the scripts to generate cvs files. Run `run_scripts/generate_cvs_files.py`
in order to accomplish this. You can then run `run_scripts/generate_graphs.py`. You must run these scripts in an environment set up with the Pulse bindings. It is suggested that you follow their guide for setup in PyCharm: https://gitlab.kitware.com/physiology/engine/-/wikis/Using-Pycharm. 



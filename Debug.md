# Pulse setup

The pulse repository requires the presence of three main applications on the path in order to build: `CMAKE`, `Java` and `Python`

## CMAKE
You have the option to download and install cmake from the website: this will also give you access to the cmake GUI (I haven't found the GUI to work very well with this) Besides you will need to manually set the path.
Install cmake using terminal commands: 'pip install cmake' should install cmake on the computer and it should be available on the path. cmake requires compilers: Either `xcode` for osx or `MinGW` for linux or windows. See below

## JAVA 
The Pulse website recommends a download from Amazon. It is possible that you are already running Java on your computer, but it may not have all the requirements. I would still recommend using amazon coretto. You need openjdk and not jre: download from [here](https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/downloads-list.html)
Ensure that JAVA_HOME is set to the downloaded openjdk path. You will need to set the path permanently. Otherwise, everytime you restart the terminal you will be required to set JAVA_HOME. The following error is associated with the path not being set correctly.
![image](https://user-images.githubusercontent.com/113397973/193475389-bdd98f59-a8b0-4130-8399-2c7682558e7d.png)


## PYTHON
Download python 3.9 and all available packages
As of November 2022, Pulse would not build correctly with Python 3.10. There are no apparent errors and the source code builds to completion but you will get a PyPulse.so file instead of the required PyPulse-cypthon-'pythonversion'-darwin.so. In python 3.9, this would be PyPulse-cypthon-39-darwin.so
Follow directions on the Pulse website to download the source code and build: [Pull and build]([https://gitlab.kitware.com/physiology/engine#building])
Make sure to enable python build by turning on cmake build of `PYTHON_API`
![image](https://user-images.githubusercontent.com/113397973/193475335-fe5d93eb-0181-40ce-a6fa-4c30f22f20d6.png)

Make sure that `XCODE` developer tools is available. Download from App Store if not available.

After a successful build, 
Update the pythonpath. The following three paths need to be available to run ecmo scripts: `export PYTHONPATH='~/Pulse/engine/src/python:~/Pulse/builds/Innerbuild/src/python:~/ecmo_pulse_scripts'`

To run a script: cd into the `install/bin` folder and type: python3 `script path`

## Pycharm
This is not mandatory, but it may be easier to work with/edit scripts. Besides, pycharm displays graphs nicely.
Download [Pycharm](https://www.jetbrains.com/pycharm/download). If you intend to use Google cloud Platform, make sure to download Pycharm Pro and activate an account.
Follow these steps to [set up](https://gitlab.kitware.com/physiology/engine/-/wikis/Using-Pycharm)the Pulse project in Pycharm.

## Virtual Instance
First, create a Google Cloud Platform [virtual machine instance](https://cloud.google.com/compute/docs/instances) Billing needs to be enabled.
Make sure that the instance has enough disk space, at least `100 GB` and `64 GB RAM`. You may have to rebuild Pulse if you increase the disk size, even after resizing.
[Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
[Add key to your VM](https://cloud.google.com/compute/docs/connect/add-ssh-keys)
`sudo` should already be available. If not try `apt install sudo`. sudo will allow you to download all the packages you need.
Install compilers: MinGW gcc and g++ C/C++ compilers
Similar steps should be followed for cmake Java and Python.

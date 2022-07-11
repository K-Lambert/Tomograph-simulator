# Tomograph-simulator
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This program, using images imported from dicom files, calculate sinogram using mathematical  formulas and then recreate image from sinogram. Program calculate detectors and emitter  position during rotation. New image can be filtered or not. It also show image recreating  process by saving and showing every tenth of tomograph step.

## Technologies
Project is created with:
* Python 3.10.5
* pydicom==2.3.0
* matplotlib==3.5.2
* numpy==1.22.3
* scikit-image==0.19.2
* scikit-learn==1.1.0
* streamlit==1.8.1
* rest and all technologies can be found in requirements.txt 

## Setup
To run program create new Virtual Environmet. To do it on Windows open command line and change your directory to your project directory and type: <br />
`python3 -m venv /path/to/new/virtual/environment` <br />
Then enter Your venv/scripts folder and then type `activate`. You should now be using your venv. Go to your project folder and install all packages by typing: <br />
`pip install -r requirements.txt` <br />
Now to run your application type: <br />
`streamlit run main.py` <br />
This will start server and should automatically start app in you browser. If that won't happen, look in your console where you find url to start app. Paste it in your browser. The app will run and it could take some time before all calculation will end. You should see that streamlit loaded sliders and calculate function. You should also see information "PROGRAM START" in your console when app will start and "PROGRAM END" when calculations will end. 


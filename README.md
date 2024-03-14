# SolarViewer
This repository contains the code for the Solar Viewer Project, part of the coursework for ENPH 454 at Queen's University. The project aims to create a system capable of tracking and observing solar eclipses using a radio telescope that can operate under varying weather conditions.

## Contributions
Contributors to this project include:
- [Ben Graham](https://github.com/bng919)
- [Devynn Garrow](https://github.com/devgarrow)
- [Nathan Ingram](https://github.com/NathanIngram2)
- [Jessica Guetre](https://github.com/jessica-guetre)
- Will Conway

## Hardware Requirements
- Raspberry Pi 3
- NEMA 23 stepper motors
- Stepper motor drivers
- LNB for frequency data reception

The TB6600 Stepper Motor Drivers are used to drive NEMA 23 Stepper Motors, while solar radiofrequency data from a linearly polarized LNB is collected and processed.

## Installation
Ensure you have Python installed on your Raspberry Pi 3. To install the necessary dependencies, run the following commands in your terminal:
```
pip install --upgrade pip # Optional
pip install astropy
pip install pandas
pip install matplotlib
pip install argparse
pip install numpy
```

## Usage
The code in this repository is structured into various modules, each serving a distinct purpose in the overall operation of the solar viewer system. The `src` directory contains the main application code, while the `exp` directory includes experimental scripts for testing and development purposes.

To run the main application:
```
cd src
python main.py
```

To test individual components, navigate to the `exp` directory and run the respective scripts:
```
cd exp
python stepperTest.py
```

Replace `stepperTest.py` with the name of the script you wish to run.

## License
SolarViewer is licensed under [GPLv3](LICENSE).

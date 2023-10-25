# Move stepper motor to limit switch in both axis, return the altitude and azmuth (0,0)
# Return: alt, az + offset
def calibrate(offset):
    
# Use astropy to calculate altitude and azmuth of sun
# Return: alt, az
def getSunPosition(lat, lon, current_time):
    
# Calculates how many degrees the stepper motor needs to move in each axis
# Return: diffAlt, diffAz
def getDifferenceDeg(antAlt, antAz, sunAlt, sunAz):

# Move stepper
# Return: null
def moveStepper(diffAlt, diffAz):
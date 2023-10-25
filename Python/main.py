from astropy.time import Time

# Constants
LAT = 
LON = 
ANT_OFFSET_AZ = 0 #or 20 for dish
STOP_TIME = 
MEAS_INTERVAL = 
MEAS_DURATION = 

antAlt, antAz = calibrate(ANT_OFFSET_AZ)

timeData = []
powerData = []

current_time = Time.now()

while(current_time < STOP_TIME):
    current_time = Time.now()
    sunAlt, sunAz = getSunPosition(LAT, LON, current_time)
    diffAlt, diffAz = getDifferenceDeg(antAlt, antAz, sunAlt, sunAz)
    moveStepper(diffAlt, diffAz)
    power = measPower(MEAS_DURATION)
    writeData(current_time, power, sunAlt, sunAz)
    timeData.append(current_time)
    powerData.append(power)
    plotPower(timeData, powerData)
    
    wait(MEAS_INTERVAL)

#Save plot

calibrate(ANT_OFFSET_AZ) # Return to zero position
import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

LIM_ALT = 7 # Limit switch 1 input from Pi
LIM_AZ = 11 # Limit switch 2 input from Pi

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(LIM_ALT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIM_AZ, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)

def calibrate(offset):
	"""
	Calibrate the stepper motor to the limit switch and return the starting altitude and azimuth.

	:param offset: Azimuth offset in degrees.
	:return: Starting altitude and azimuth of the antenna in degrees. (0,0)
	"""
	print("Starting Calibration...")
	GPIO.output(DIR, CCW)
	# Altitude calibration
	while(GPIO.input(LIM_ALT) != GPIO.HIGH):
		# Run for 200 steps. This will change based on how you set you controller
		for x in range(10):
			# Set one coil winding to high
			GPIO.output(STEP,GPIO.HIGH)
			# Allow it to get there.
			sleep(.005) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run
		

	sleep(5) # Dictates how fast stepper motor will run
	GPIO.output(DIR, CW)

	# Azimuth calibration
	while(GPIO.input(LIM_AZ) != GPIO.HIGH):
		# Run for 200 steps. This will change based on how you set you controller
		for x in range(10):
			# Set one coil winding to high
			GPIO.output(STEP,GPIO.HIGH)
			# Allow it to get there.
			sleep(.005) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run

	GPIO.output(DIR, CCW)
	return 0, offset


try:
	calibrate(0)
	

# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()




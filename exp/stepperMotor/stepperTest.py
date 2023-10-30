import pigpio as GPIO
from time import sleep

# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Needs to be initalized before any other commands
pi = GPIO.pi()
if not pi.connected:
    exit()

# ------------------------------------------------
# Setup pin layout on PI
# GPIO.setmode(GPIO.BOARD)	replacement for this???
# ------------------------------------------------

pi.set_mode(GPIO, GPIO.OUTPUT)

# Establish Pins in software
pi.set_mode(DIR, GPIO.OUT)
pi.set_mode(STEP, GPIO.OUT)

# Set the first direction you want it to spin
pi.write(DIR, CW)

try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		# Esablish the direction you want to go
		pi.write(DIR,CW)

		# Run for 200 steps. This will change based on how you set you controller
		for x in range(200):

			# Set one coil winding to high
			pi.write(STEP,GPIO.HIGH)
			# Allow it to get there.
			sleep(.005) # Dictates how fast stepper motor will run
			# Set coil winding to low
			pi.write(STEP,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		pi.write(DIR,CCW)
		for x in range(200):
			pi.write(STEP,GPIO.HIGH)
			sleep(.005)
			pi.write(STEP,GPIO.LOW)
			sleep(.005)

# Once finished clean everything up
except KeyboardInterrupt:
	print("Stop and release GPIO resources.")
	pi.stop()
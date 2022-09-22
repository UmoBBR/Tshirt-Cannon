#import maestro

# For motor controllers, servo speed setting dampens acceleration (acts like inertia).
# Higher values will reduce inertia (try values around 50 to 100) 
INERTIA = 200
#

class DriveTrain:
        # Init drive train, passing maestro controller obj, and channel
        # numbers for the motor servos Left and Right
	def __init__(self, maestro,chLeft,chRight,chLeft2,chRight2):
		self.maestro = maestro
		self.chRight = chRight
		self.chLeft = chLeft
		self.chRight2 = chRight2
		self.chLeft2 = chLeft2
		# Init motor accel/speed params
		self.maestro.setAccel(chRight,0)
		self.maestro.setAccel(chLeft,0)
		self.maestro.setAccel(chRight2,0)
		self.maestro.setAccel(chLeft2,0)
		self.maestro.setSpeed(chRight,INERTIA)
		self.maestro.setSpeed(chLeft,INERTIA)
		self.maestro.setSpeed(chRight2,INERTIA)
		self.maestro.setSpeed(chLeft2,INERTIA)
		# Right motors min/center/max vals
		self.minR = 2760
		self.centerR = 6000
		self.maxR = 9300
		self.minR2 = 2760
		self.centerR2 = 6000
		self.maxR2 = 9300
		# Left motors min/center/max vals
		self.minL = 2760
		self.centerL = 6000
		self.maxL = 9300
		self.minL2 = 2760
		self.centerL2 = 6000
		self.maxL2 = 9300
		

	# Mix joystick inputs into motor L/R mixes
	def arcadeMix(self, joyX, joyY):
		r = 1 * joyX
		l = joyY
		v = (1 - abs(r)) * l + l
		w = (1 - abs(l)) * r + r
		motorR = -(v + w) / 2  
		motorR2 = -(v + w) / 2  
		motorL = (v - w) / 2
		motorL2 = (v - w) / 2
		return (motorR, motorL, motorR2, motorL2)

	# Scale motor speeds (-1 to 1) to maestro servo target values
	def maestroScale(self, motorR, motorL, motorR2, motorL2):
		if (motorR >= 0) :
			r = int(self.centerR + (self.maxR - self.centerR) * motorR)
		else:
			r = int(self.centerR + (self.centerR - self.minR) * motorR)
		if (motorR2 >= 0) :
			r2 = int(self.centerR2 + (self.maxR2 - self.centerR2) * motorR2)
		else:
			r2 = int(self.centerR2 + (self.centerR2 - self.minR2) * motorR2)
		if (motorL >= 0) :
			l = int(self.centerL + (self.maxL - self.centerL) * motorL)
		else:
			l = int(self.centerL + (self.centerL - self.minL) * motorL)
		if (motorL2 >= 0) :
			l2 = int(self.centerL2 + (self.maxL2 - self.centerL2) * motorL2)
		else:
			l2 = int(self.centerL2 + (self.centerL2 - self.minL2) * motorL2)
		return (r, l, r2, l2)

	# Blend X and Y joystick inputs for arcade drive and set servo
	# output to drive motor controllers
	def drive(self, joyX, joyY):
		(motorR, motorL, motorR2, motorL2) = self.arcadeMix(joyX, joyY)
		(servoR, servoL, servoR2, servoL2) = self.maestroScale(motorR, motorL, motorR2, motorL2)
		#print "Target R = ",servoR
		self.maestro.setTarget(self.chRight, servoR)
		self.maestro.setTarget(self.chLeft, servoL)
		self.maestro.setTarget(self.chRight2, servoR2)
		self.maestro.setTarget(self.chLeft2, servoL2)

	# Set both motors to stopped (center) position
	def stop(self):
		self.maestro.setTarget(self.chRight, self.centerR)
		self.maestro.setTarget(self.chLeft, self.centerL)
		self.maestro.setTarget(self.chRight2, self.centerR2)
		self.maestro.setTarget(self.chLeft2, self.centerL2)

	# Close should be used when shutting down Drive object
	def close(self):
		self.stop()

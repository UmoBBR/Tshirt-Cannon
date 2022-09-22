import PiIO
import maestro
import xbox
import drive
import time

# CONSTANTS
LEFT_MOTORS = 1
RIGHT_MOTORS = 0
LEFT_MOTORS2 = 3
RIGHT_MOTORS2 = 2
THROWER = 4
CAM = 5
THROWER_MAX = 9200
THROWER_STOP = 6000
THROWER_RANGE = 3200
CAM_FWD = 2760
CAM_REV = -9300
CAM_STOP = 6000

# VARIABLES
speedToggle = 2 # 2 = Full Speed; 1 = Slow Mode; 0 = Driving Disabled 
currentThrower = 7600 # Initial thrower set to 50% power

# BOOLEANS
isStarted = False # Press Start to enable the robot
compressorEnabled = False
PressedY = False # Allows Y to be called on rising edge
throwerEnabled = False
pressedA = False # Allows A to be called on rising edge
pressedBack = False # Allows Back to be called on rising edge


j = xbox.Joystick()
motors = maestro.Controller()
drive = drive.DriveTrain(motors, LEFT_MOTORS, RIGHT_MOTORS, LEFT_MOTORS2, RIGHT_MOTORS2)

try:
    cannonr      = PiIO.Spike(1)
    
except:
    raise
# **MAINE LOOP**

print "Bot rises!"
print "Press Start to enable."
try:
    while True:

        if isStarted:

            ### Drive Command ###
            if speedToggle != 0:
                if speedToggle == 2:
                    if abs(j.leftX()) <= .10 and abs(j.leftY()) <= .21:
                        drive.drive(0, 0)
                    else:
                        drive.drive(j.leftX(), -j.leftY())
                else:
                    if abs(j.leftX()) <= .15 and abs(j.leftY()) <= .23:
                        drive.drive(0, 0)
                    else:
                        drive.drive(j.leftX(), -j.leftY() * .4)    
            else:
                drive.drive(0, 0)

            ### Speed toggle & Drive Control ###
            if j.X():
                #print "FULL SPEED AHEAD!"
                pressedBack = True
                speedToggle = 2
            if j.B():
                speedToggle = 1
                #print "Slow Driving Mode"
                pressedBack = True

            ### Speed Of Thrower Motor ###
            if throwerEnabled == False and speedToggle == 2:
                if j.leftTrigger() >= .20 and j.leftTrigger() < .40:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .50)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .50))
                    #print "Thrower: 50%"
                elif j.leftTrigger() >= .40 and j.leftTrigger() < .60:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .65)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .65))
                    #print "Thrower: 65%"
                elif j.leftTrigger() >= .60 and j.leftTrigger() < .80:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .80)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .80))
                    #print "Thrower: 80%"
                elif j.leftTrigger() >= .80:
                    motors.setTarget(THROWER, THROWER_MAX)
                    currentThrower = THROWER_MAX
                    #print "Thrower: MAX POWER!!!"
                else:
                    motors.setTarget(THROWER, THROWER_STOP)

            ### Lock and Recall Thrower Speed ###    
            if j.A():
                if pressedA == False:
                    if throwerEnabled == False:
                        motors.setTarget(THROWER, currentThrower)
                        throwerEnabled = True
                        #print "throwerEnabled = True"
                    else:
                        motors.setTarget(THROWER, THROWER_STOP)
                        throwerEnabled = False
                        #print "throwerEnabled = False"
                    pressedA = True
            else:
                pressedA = False

            #UP DOWN
            if j.rightBumper():
                motors.setTarget(CAM, CAM_FWD)
                #print "FWD" + str(j.rightX())
            elif j.leftBumper():
                motors.setTarget(CAM, CAM_REV)
                #print "REV" + str(j.rightX())
            else:
                motors.setTarget(CAM, CAM_STOP)

            if j.rightTrigger():
                 cannonr.fwd()
            else:
                cannonr.stop()
                
        ### Robot Start Boolean ###
        if j.Start():
            isStarted = True
            #print "Start"

        # Time interval before next loop begins.
        time.sleep(0.033)
except:
        #winch.stop()
        motors.setTarget(CAM, CAM_STOP)
        motors.setTarget(THROWER, THROWER_STOP)
        #compressor.stop()
        drive.close()
        motors.close()
        j.close()
        PiIO.close()
        raise

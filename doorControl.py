import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time
import ifttNotification

doorIsOpening = False
doorIsClosing = False

gPotPin = None
gAdc = None
gGain = None
gSafeMaxVoltage = None
gSafeMinVoltage = None
gDangerMaxVoltage = None
gDangerMinVoltage = None
gPotOpenDirection = None
gPotClosedDirection = None

gMotorPin = None
gSpeed = None
gMaxTime = None
gMotorOpenDirection = None
gMotorClosedDirection = None
gPwm = None

def setupMotorControl( gpioMotorPin, speed, maxTime, openDirection  ) :
	global gMotorPin
	global gSpeed
	global gMaxTime
	global gMotorOpenDirection
	global gMotorClosedDirection
	global gPwm
	
	gMotorPin = gpioMotorPin
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(motorPin,GPIO.OUT)	
	gPwm=GPIO.PWM(motorPin,50)
	gMotorOpenDirection = openDirection
	gMotorClosedDirection = -1 * openDirection
	gMaxTime = maxTime
	gSpeed = speed
	
def setupDoorSensor( adcPotPin, openDirection, safeMaxVoltage, safeMinVoltage, dangerMaxVoltage, dangerMinVoltage )
	global gPotPin
	global gAdc
	global gGain
	global gSafeMaxVoltage
	global gSafeMinVoltage
	global gDangerMaxVoltage
	global gDangerMinVoltage
	global gPotOpenDirection
	global gPotClosedDirection
	
	gPotPin = adcPotPint
	gGain = 1
	gAdc = adc.read_adc(gPotPin, gGain)
	gDangerMaxVoltage = dangerMaxVoltage
	gDangerMinVoltage = dangerMinVoltage
	gSafeMinVoltage = safeMinVoltage
	gSafeMaxVoltage = safeMaxVoltage
	gPotOpenDirection = openDirection
	gPotClosedDirection = -1 * openDirection
	
def openDoor()
	if gAdc == None or gPwm == None :
		raise Exception("Call setupDoorSensor and/or setupMotorControl first")
		
	if isDoorOpen() :
		print 'Door is already open!'
		return 

	startTime = time.clock();
	currentTime = time.clock();
	runningTime = currentTime - startTime;
	
	gPwm.start( motorSpeedToDutyCycle( gSpeed * gMotorOpenDirection ) )

	global doorIsOpening
	doorIsOpening = True

	while !isDoorOpen() and runningTime < gMaxTime :
		currentTime = time.clock()
		runningTime = currentTime - startTime
		time.sleep(0.005)

	gPwm.stop()
	
	if isDoorOpen() :
		if __debug__:
			print 'Door is now open'
	else "
		if __debug__:
			print 'Motor timeout'
			ifttNotification.sendDoorEmailNotification('Opening', getDoorOpenPercentage() )

	doorIsOpening = False;
	
def closeDoor()
	if gAdc == None or gPwm == None :
		raise Exception("Call setupDoorSensor and/or setupMotorControl first")
		
	if isDoorClosed() :
		print 'Door is already closed!'
		return 

	startTime = time.clock();
	currentTime = time.clock();
	runningTime = currentTime - startTime;
	
	gPwm.start( motorSpeedToDutyCycle( gSpeed * gMotorClosedDirection ) )

	global doorIsClosing
	doorIsClosing = True

	while !isDoorClosed() and runningTime < gMaxTime :
		currentTime = time.clock()
		runningTime = currentTime - startTime
		time.sleep(0.005)

	gPwm.stop()
	
	if isDoorClosed() :
		if __debug__:
			print 'Door is now open'
	else "
		if __debug__:
			print 'Motor timeout'
			ifttNotification.sendDoorEmailNotification('Closing', getDoorOpenPercentage() )

	doorIsClosing = False;

def isDoorOpen()
	if gAdc == None :
		raise Exception("Call setupDoorSensor first")

	percent = getDoorOpenPercentage()
	if percent > 100.0
		print 'Pot sensor is outside the safe range! STOP!'
		return True
	if percent < 0.0 
		print 'Pot sensor is outside the safe range! STOP!'
		if doorIsOpening :
			#stop the door trying to open!
			return True
		else :
			return False
			
	return percent == 100.0
	
def isDoorClosed()
	if gAdc == None :
		raise Exception("Call setupDoorSensor first")
		
	percent = getDoorOpenPercentage()
	if percent < 0.0
		print 'Pot sensor is outside the safe range! STOP!'
		return True
	if percent > 100.0 
		print 'Pot sensor is outside the safe range! STOP!'
		if doorIsClosing :
			#stop the door trying to close!
			return True
		else :
			return False
			
	return percent == 0.0

def getPotReading()
	if gAdc == None :
		raise Exception("Call setupDoorSensor first")
		
	sensorValue = gAdc.read_adc(gPotPin, gGain)
	voltage = sensorValue * (4.096/4095)
	return voltage
	
def getDoorOpenPercentage()
	if gAdc == None :
		raise Exception("Call setupDoorSensor first")
		
	voltage = getPotReading()
	percent = (voltage - gSafeMinVoltage) / (gSafeMaxVoltage - gSafeMinVoltage)
	if doorOpenSensorDirection == -1.0 :
		percent = 1 - percent

	percent = percent * 100
	return percent

def motorSpeedToDutyCycle( motorSpeed )
	if gPwm == None :
		raise Exception("Call setupMotorControl first")
		
	#Motor speed should be between -255 and 255
	#But we need to convert to a duty cycle for the servo/VEX motor controller 29
	#DutyCycle = PulseWidth/(1/frequency) = PulseWidth * frequency
	#frequency is 50hz
	#1.0, 1.5, and 2.0ms for rev, off, and fwd
	#-255 = 1.0ms and 255 = 2.0ms
	#510 = 1.0 ms.
	pulseWidth = ((( motorSpeed + 255 ) / 510)  + 1 ) *0.001
	dutyCycle = pulseWidth * 50
	#duty cycle is calcuated as a decimal, but should be returned as a percent
	return dutyCycle * 100
	

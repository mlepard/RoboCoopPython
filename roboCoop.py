import sunAndTime
import temperatureControl
import doorControl
import RPi.GPIO as GPIO 

heaterPin = 23
temperaturePin = 11
motorPin = 24
potPin = 2 

printDebug = True

def setupRoboCoop():
	GPIO.setwarnings(False)
	sunAndTime.initSunAndTime()
	temperatureControl.initTempControl(temperaturePin,heaterPin)
	doorControl.setupDoorSensor(potPin, 1, 1800, 560, 1950, 318)
	doorControl.setupMotorControl(motorPin, 255, 4.0, 1)
	
	sunAndTime.printDebug = printDebug
	
def maintainTemperature(lowTemp, highTemp):
	currentTemp = temperatureControl.getTemperature()
	if __debug__:
		print 'Current {}  Low {}  High {}'.format(currentTemp, lowTemp, highTemp)	
	if currentTemp < lowTemp :
		print "Low temp, turning heater on..."
		temperatureControl.turnHeaterOn()
	elif currentTemp > highTemp :
		print "High temp, turning heater off..."
		temperatureControl.turnHeaterOff()

def doDoorControl():
	try:
		if sunAndTime.isDoorOpenTimeNow() and not doorControl.isDoorOpen() :
			if not doorControl.openDoor() :
				import ifttNotification
				ifttNotification.sendDoorEmailNotification('Opening', getDoorOpenPercentage() )
			return
			
		if sunAndTime.isDoorCloseTimeNow() and not doorControl.isDoorClosed() :
			if not doorControl.closeDoor() :
				import ifttNotification
				ifttNotification.sendDoorEmailNotification('Closing', getDoorOpenPercentage() )
			return
	except PotSensorError as e:
		import ifttNotification
		ifttNotification.sendDoorEmailNotification('Pot Sensor Error', e.args[0] )
		return
		
def getDoorPercentageOpen():
	return doorControl.getDoorOpenPercentage()
	
def cleanup():
	doorControl.stopMotor()

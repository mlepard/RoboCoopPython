import sunAndTime
import temperatureControl
import doorControl
import RPi.GPIO as GPIO 

heaterPin = 15
temperaturePin = 4
motorPin = 14
potPin = 3 

def setupRoboCoop():
	GPIO.setwarnings(False)
	sunAndTime.initSunAndTime()
	temperatureControl.initTempControl(4,15)
	doorControl.setupDoorSensor(3, 1, 1800, 769, 1950, 318)
	doorControl.setupMotorControl(14, 255, 3.0, 1)
	
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
	if sunAndTime.isDoorOpenTimeNow() and not doorControl.isDoorOpen() :
		doorControl.openDoor()
		return
		
	if sunAndTime.isDoorClosedTimeNow() and not doorControl.isDoorClosed() :
		doorControl.closeDoor()
		return
		
def getDoorPercentageOpen():
	return doorControl.getDoorOpenPercentage()
	
def cleanup():
	doorControl.stopMotor()
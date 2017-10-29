import roboCoop
import doorControl

#temperatureControl.initTempControl(4, 15)
#print temperatureControl.getTemperature()
#temperatureControl.turnHeaterOff()

#doorControl.setupDoorSensor(3, 1, 1935, 769, 2035, 518)
#doorControl.setupMotorControl(14, 255, 2.0, 1)
#print "opening door"
#doorControl.openDoor()
#import temperatureControl

try:
	roboCoop.setupRoboCoop()
	#roboCoop.maintainTemperature(10, 15)
	#print roboCoop.getDoorPercentageOpen()
	doorControl.openDoor()
	doorControl.closeDoor()

finally:
	roboCoop.cleanup()

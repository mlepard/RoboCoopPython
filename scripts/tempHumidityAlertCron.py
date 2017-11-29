import os
scriptPath = os.path.realpath(__file__)
scriptPath = os.path.dirname(scriptPath)
modulePath = os.path.split(scriptPath)[0]
import sys
sys.path.append(modulePath)

import roboCoop
import temperatureControl

try:
	roboCoop.setupRoboCoop()
	temp, humidity = temperatureControl.getTemperatureAndHumidity()
	if temp < -25:
		import ifttNotification
		ifttNotification.sendLowTempNotification(temp)
	if temp < -5 and humidity > 75:
		import ifttNotification
		ifttNotification.sendHighHumidityEmailNotification(humidity)


finally:
	roboCoop.cleanup()
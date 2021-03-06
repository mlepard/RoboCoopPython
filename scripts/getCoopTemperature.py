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
	heater = ""
	if temperatureControl.isHeaterOn():
		heater = "ON"
	else:
		heater = "OFF"
	print 'Coop is at {:.1f}C.'.format(temp) + ' Heater is ' + heater
	print 'Coop Humidity is {:.0f}%.'.format(humidity)

finally:
	roboCoop.cleanup()

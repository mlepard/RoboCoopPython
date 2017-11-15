import os
scriptPath = os.path.realpath(__file__)
scriptPath = os.path.dirname(scriptPath)
modulePath = os.path.split(scriptPath)[0]
import sys
sys.path.append(modulePath)

import roboCoop
import sunAndTime

try:
	roboCoop.setupRoboCoop()
	roboCoop.maintainTemperature(-15, -10)
	roboCoop.doDoorControl()

finally:
	roboCoop.cleanup()

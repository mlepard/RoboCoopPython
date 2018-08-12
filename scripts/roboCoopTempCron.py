import os
scriptPath = os.path.realpath(__file__)
scriptPath = os.path.dirname(scriptPath)
modulePath = os.path.split(scriptPath)[0]
import sys
sys.path.append(modulePath)

import roboCoop

try:
	roboCoop.setupRoboCoop()
	roboCoop.maintainTemperature(28.0, 32.0)

finally:
	roboCoop.cleanup()

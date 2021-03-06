import os
scriptPath = os.path.realpath(__file__)
scriptPath = os.path.dirname(scriptPath)
modulePath = os.path.split(scriptPath)[0]
import sys
sys.path.append(modulePath)

import sunAndTime
sunAndTime.initSunAndTime()

if sunAndTime.isDoorOpenTimeNow() or sunAndTime.isDoorCloseTimeNow():
	import roboCoop
	try:
		roboCoop.setupRoboCoop()
		roboCoop.doDoorControl()
	finally:
		roboCoop.cleanup()
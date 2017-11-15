import os
scriptPath = os.path.realpath(__file__)
scriptPath = os.path.dirname(scriptPath)

modulePath = os.path.split(scriptPath)[0]

import sys
sys.path.append(modulePath)

import roboCoop
import doorControl

try:
	roboCoop.setupRoboCoop()
	doorControl.closeDoor()
	print 'Door is at {}'.format(doorControl.getDoorOpenPercentage())

finally:
	roboCoop.cleanup()

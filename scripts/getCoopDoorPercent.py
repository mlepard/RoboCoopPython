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
	percent = doorControl.getDoorOpenPercentage()
	state = "Middle"
	if percent < 10 :
		state = "Closed"
	elif percent > 90 :
		state = "Open"
	print 'Door is {} at {}'.format(state, percent)

finally:
	roboCoop.cleanup()

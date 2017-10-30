import roboCoop
import doorControl

try:
	roboCoop.setupRoboCoop()
	percent = doorControl.getDoorOpenPercentage()
	state = ""
	if percent < 10 :
		state = "Closed"
	elif percent > 90 :
		state = "Open"
	print 'Door is {} at {}'.format(state, percent)

finally:
	roboCoop.cleanup()

import roboCoop
import doorControl

try:
	roboCoop.setupRoboCoop()
	doorControl.closeDoor()
	print 'Door is at {}'.format(doorControl.getDoorOpenPercentage())

finally:
	roboCoop.cleanup()

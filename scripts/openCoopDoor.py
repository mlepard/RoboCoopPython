import roboCoop
import doorControl

try:
	roboCoop.setupRoboCoop()
	doorControl.openDoor()
	print 'Door is at {}'.format(doorControl.getDoorOpenPercentage())

finally:
	roboCoop.cleanup()

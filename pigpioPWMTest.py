import pigpio
import time

SERVO = 14

MIN_PW = 1000
MID_PW = 1500
MAX_PW = 2000

pi = pigpio.pi()

pulsewidth = MAX_PW



pi.set_servo_pulsewidth(SERVO, 1600)
pi.set_PWM_frequency(SERVO, 50)

#pi.stop()
try: 
	while True:
		time.sleep(0.001)

		
finally:
	pi.set_servo_pulsewidth(SERVO, 0)
	pi.stop()

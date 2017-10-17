import Adafruit_DHT
import RPi.GPIO as GPIO

def initTempControl(tempPin, heaterPin):
	global __DHT_PIN__  = None # add this line!
	global __DHT_TYPE__ = Adafruit_DHT.DHT22
	if __DHT_PIN__ is None: # see notes below; explicit test for None
		__DHT_PIN__ = tempPin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(__DHT_PIN__, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	else:
		raise RuntimeError("Temperature Control already initialized...")
		return
	
	global __Heater_Pin__ = None
	if __Heater_Pin__ is None:
		__HeaterPin__ = heaterPin
		GPIO.setup(__HeaterPin__, GPIO.OUT)
		GPIO.output(__HeaterPin__, 0)
	else:
		raise RuntimeError("Temperature Control already initialized...")
		return
		
def getTemperature()
	if __DHT_PIN__ is None:
		print "initTempControl not called..."
		return None
	#get the current temperature
	humidity, temp = Adafruit_DHT.read_retry(__DHT_TYPE__, __DHT_PIN__)
	if temp is None:
		print "Can't get temp, exiting..."
	return temp
	
def turnHeaterOn()
	if __Heater_Pin__ is None:
		print "initTempControl not called..."
		return
	GPIO.output(__HeaterPin__, 1)
	
def turnHeaterOff()
	if __Heater_Pin__ is None:
		print "initTempControl not called..."
		return
	GPIO.output(__HeaterPin__, 0)	
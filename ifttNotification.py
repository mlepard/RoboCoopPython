class MakerTrigger(object):
  def __init__(self,key,trigger):
    self.key = key
    self.trigger = trigger
    self.maker = "https://maker.ifttt.com/trigger/" + self.trigger + "/with/key/" + self.key
  def alert(self,value1=0,value2=0,value3=0):
    import requests
    self.value1 = value1
    self.value2 = value2
    self.value3 = value3
    self.json={"value1" : self.value1, "value2" : self.value2, "value3" : self.value3}
    r = requests.post(self.maker, json=self.json)

def sendDoorEmailNotification( door_action, door_status) :
	key = "dFF3dgc7zX2Cas6ipyRuy1"
	trigger = "coop_door_failure"
	ifttt = MakerTrigger(key,trigger)
	ifttt.alert(door_action,door_status)
	
def sendLowTempEmailNotification( temperature ) :
	key = "dFF3dgc7zX2Cas6ipyRuy1"
	trigger = "coop_low_temperature"
	ifttt = MakerTrigger(key,trigger)
	ifttt.alert(temperature)
	
def sendHighHumidityEmailNotification( humidity ) :
	key = "dFF3dgc7zX2Cas6ipyRuy1"
	trigger = "coop_high_humidity"
	ifttt = MakerTrigger(key,trigger)
	ifttt.alert(humidity)	
	

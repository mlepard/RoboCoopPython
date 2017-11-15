from datetime import datetime
import time

printDebug = False

class Date :
	def __init__(self, value1, value2):
		self.month = value1
		self.day = value2
	
	def toString(self):
		return '{}/{}'.format(self.month, self.day)
	
class Time :
	def __init__(self, value1, value2):
		self.hour = value1
		self.minute = value2		

	def toString(self): 
		return '{}:{:02d}'.format(int(self.hour), int(self.minute))

	def toLocalTZString(self): 
		localTime = convertUTCToLocalTime(self)
		return '{}:{:02d}'.format(int(localTime.hour), int(localTime.minute))
		
	def subtractTime(self, time):
		result = Time(0, 0)
		wMinute = self.minute - time.minute
		wHour = self.hour - time.hour
		if wMinute < 0 :
			wHour = wHour - 1
			wMinute = wMinute + 60
		if wHour < 0 :
			wHour = wHour + 24
		result.hour = int(wHour)
		result.minute = int(wMinute)
		return result

	def addTime(self, time):
		result = Time( 0, 0 )
		wMinute = (self.minute + time.minute);
		wHour = (self.hour + time.hour);
		if wMinute >= 60 :
			wMinute = wMinute - 60
			wHour = wHour + 1
		if result.hour > 24 :
			wHour = wHour - 24
		result.hour = int(wHour)
		result.minute = int(wMinute)
		return result
		
	def equal(self, time):
		if printDebug:
			print 'Compare Time: Self is {}:{:02d} and Value is {}:{:02d} '.format( int(self.hour), int(self.minute), int(time.hour), int(time.minute))
	
		if self.hour == time.hour and self.minute == time.minute :
			return True
		else :
			return False
	
class SunRiseAndSetData :
	def __init__(self, date, sunRise, sunSet, riseDelta, setDelta):
		if not isinstance(date, Date): 
			raise Exception("SunRiseAndSetData init error, date not a Date")
		self.startDate = date
		if not isinstance(sunRise, Time): 
			raise Exception("SunRiseAndSetData init error, sunRise not a Time")
		self.sunRise = sunRise
		if not isinstance(sunSet, Time): 
			raise Exception("SunRiseAndSetData init error, sunSet not a Time")
		self.sunSet = sunSet
		try:
			int(riseDelta)
		except ValueError:
				raise Exception("SunRiseAndSetData init error, riseDelta not a int")
		else:
			self.sunriseDelta = riseDelta
		try:
			int(setDelta)
		except ValueError:
				raise Exception("SunRiseAndSetData init error, setDelta not a int")
		else:
			self.sunsetDelta = setDelta

	def toString(self):
		return 'Date: {} SunRise: {} SunSet: {} RiseDelta: {} SetDelta: {}'.format(self.startDate.toString(), self.sunRise.toLocalTZString(), self.sunSet.toLocalTZString(), self.sunriseDelta, self.sunsetDelta) 

def initSunAndTime():
	global sunData
	sunData = []
	#Note, these times are in Eastern Daylight Time.
	#We'll convert to UTC in the code to avoid issues with daylight savings.
	initData =  [[ [1,  1 ],  [8, 42, 0],  [17, 31, 0],  -4,  15 ],
				[ [1,  16],  [8, 37, 0],  [17, 48, 0],  -14, 21 ],
				[ [2,  1 ],  [8, 22, 0],  [18, 10, 0],  -20, 20 ],
				[ [2,  16],  [8, 01, 0],  [18, 32, 0],  -20, 17 ],
				[ [3,  1 ],  [7, 39, 0],  [18, 50, 0],  -26, 19 ],
				[ [3,  16],  [7, 11, 0],  [19, 10, 0],  -28, 20 ],
				[ [4,  1 ],  [6, 41, 0],  [19, 31, 0],  -26, 18 ],
				[ [4,  16],  [6, 13, 0],  [19, 50, 0],  -22, 18 ],
				[ [5,  1 ],  [5, 49, 0],  [20, 10, 0],  -18, 17 ],
				[ [5,  16],  [5, 30, 0],  [20, 28, 0],  -13, 15 ],
				[ [6,  1 ],  [5, 17, 0],  [20, 44, 0],  -4,  9 ],
				[ [6,  16],  [5, 13, 0],  [20, 53, 0],  5,   2 ],
				[ [7,  1 ],  [5, 18, 0],  [20, 54, 0],  11, -7 ],
				[ [7,  16],  [5, 30, 0],  [20, 47, 0],  16, -16 ],
				[ [8,  1 ],  [5, 48, 0],  [20, 30, 0],  16, -21 ],
				[ [8,  16],  [6, 05, 0],  [20, 07, 0],  19, -26 ],
				[ [9,  1 ],  [6, 25, 0],  [19, 39, 0],  17, -27 ],
				[ [9,  16],  [6, 43, 0],  [19, 11, 0],  17, -27 ],
				[ [10, 1 ],  [7, 02, 0],  [18, 42, 0],  18, -26 ],
				[ [10, 16],  [7, 21, 0],  [18, 14, 0],  20, -24 ],
				[ [11, 1 ],  [7, 43, 0],  [17, 49, 0],  19, -17 ],
				[ [11, 16],  [8, 04, 0],  [17, 31, 0],  17, -10 ],
				[ [12, 1 ],  [8, 23, 0],  [17, 21, 0],  13, -1  ],
				[ [12, 16],  [8, 36, 0],  [17, 20, 0],  6,  9   ],
		]
	
	for item in initData:
		initDate = Date( item[0][0], item[0][1] )
		#convert hours to UTC
		initSunRise = Time( item[1][0] + 4, item[1][1] )
		initSunSet = Time( item[2][0] + 4, item[2][1] )
		sunriseData = SunRiseAndSetData( initDate, initSunRise, initSunSet, item[3], item[4] )
		sunData.append( sunriseData )
					
def getDoorOpenTime() :
	currentDate = datetime.now()
	currentSunData = getSunRiseAndSetData( currentDate )
	deltaDate = 0
	if currentDate.day > 15:
		deltaDate = 31 - currentDate.day;
		deltaDate = 1.0 - deltaDate / 15.0;
	else:
		deltaDate = 15 - currentDate.day;
		deltaDate = 1.0 - deltaDate / 15.0;

	dateDeltaTime = Time(0, 0);
	if currentSunData.sunriseDelta < 0 :
		temp =  deltaDate * (-1.0*currentSunData.sunriseDelta)
		dateDeltaTime.minute = temp
		doorOpenTime = currentSunData.sunRise.subtractTime( dateDeltaTime )
	else:
		temp =  deltaDate * (currentSunData.sunriseDelta)
		dateDeltaTime.minute = temp
		doorOpenTime = currentSunData.sunRise.addTime( dateDeltaTime )

	#doorOpenTime = addTime( doorOpenTime, sunriseExtraTime );
	if printDebug:
		print 'DateDeltaTime is: {} '.format(dateDeltaTime.toString())
		print 'DoorOpenTime is: {} '.format(doorOpenTime.toLocalTZString())
			
	return doorOpenTime

def getDoorCloseTime() :
	currentDate = datetime.now()
	currentSunData = getSunRiseAndSetData( currentDate );

	deltaDate = 0
	if currentDate.day > 15 :
		deltaDate = 31 - currentDate.day
		deltaDate = 1.0 - deltaDate / 15.0
	else :
		deltaDate = 15 - currentDate.day
		deltaDate = 1.0 - deltaDate / 15.0;

	dateDeltaTime = Time(0, 0)
	if currentSunData.sunsetDelta < 0 :
		temp =  deltaDate * (float)(-1*currentSunData.sunsetDelta)
		dateDeltaTime.minute = temp;
		doorCloseTime = currentSunData.sunSet.subtractTime( dateDeltaTime )
	else :
		temp =  deltaDate * (float)(currentSunData.sunsetDelta)
		dateDeltaTime.minute = temp;
		doorCloseTime = currentSunData.sunSet.addTime( dateDeltaTime )

	#doorCloseTime = addTime( doorCloseTime, sunsetExtraTime );
	if printDebug:
		print 'DateDeltaTime is: {} '.format(dateDeltaTime.toString())
		print 'DoorCloseTime is: {} '.format(doorCloseTime.toLocalTZString())
		
	return doorCloseTime;  

	
def getSunRiseAndSetData( currentDate ) :
	global sunData
	index = 2 * (currentDate.month - 1)
	deltaDate = 0.0
	if currentDate.day > 15 :
		index = index + 1
		deltaDate = 31 - currentDate.day
		deltaDate = 1.0 - deltaDate / 15.0
	else :
		deltaDate = 15 - currentDate.day
		deltaDate = 1.0 - deltaDate / 15.0
		
	currentSunData = sunData[index]
	
	if printDebug:
		print  'Todays SunData: {}'.format(currentSunData.toString())
	
	return currentSunData

def convertUTCToLocalTime( currentTime ) :
	if time.localtime().tm_isdst:
		delta = 4
	else:
		delta = 5
	localTime = Time( currentTime.hour - delta, currentTime.minute )
	return localTime
	
def isDoorOpenTimeNow() :
	currentUTC = datetime.utcnow()
	utcTime = Time( currentUTC.hour, currentUTC.minute )
	doorOpenTime = getDoorOpenTime()
	return utcTime.equal(doorOpenTime)
	
def isDoorCloseTimeNow() :
	currentUTC = datetime.utcnow()
	utcTime = Time( currentUTC.hour, currentUTC.minute )
	doorCloseTime = getDoorCloseTime()
	return utcTime.equal(doorCloseTime)	
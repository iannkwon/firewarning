#sudo apt-get install python dev python rpi.gpio
import RPi.GPIO as GPIO
import time, datetime
import urllib.request

GPIO.setmode(GPIO.BCM)

GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4,GPIO.OUT)
GPIO.output(4,False)

print("Fire")
 
try:
	while True :
		while GPIO.input(24) == False :
			time.time()
			GPIO.output(4, False)
		while GPIO.input(24) == True :
			now = time.localtime()
			fdate = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
			
			fsignal = "On"	
			url = 'http://192.168.0.135:8090/webPython/insertOK.do'
			data = urllib.parse.urlencode({'fdate':fdate,'fsignal':fsignal})
			data = data.encode('utf-8')
			req1 = urllib.request.Request(url)
			response = urllib.request.urlopen(url,data)
			result = response.read().decode("utf-8")
			print(result)			

			time.time()
			print("Fire On",fdate)
			while True :
				
				GPIO.output(4, True)
				if (GPIO.input(27) == True) :
					now = time.localtime()
					fdate = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
					fsignal = "Off"
					url = 'http://192.168.0.135:8090/webPython/insertOK.do'
					data = urllib.parse.urlencode({'fdate':fdate,'fsignal':fsignal})
					data = data.encode('utf-8')
					req1 = urllib.request.Request(url)
					response = urllib.request.urlopen(url,data)
					
					print("LED trun off",fdate)
					
					break		
		
except KeyboardInterrupt :
	print("GPIO.cleanup()")
	GPIO.cleanup()


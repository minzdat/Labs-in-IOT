import time
import network
from machine import Pin
import BlynkLib

BLYNK_AUTH = "EtYdkLhAaHAdHYlY6n9p82ILMvQI5Uxn"
blynk = BlynkLib.Blynk(BLYNK_AUTH)

led = Pin(2, Pin.OUT)
@blynk.on("V0") #virtual pin V0
def v0_read_handler(value): #read the value
	if int(value[0]) == 0:
		led.value(0) #turn the led on
	else:
		led.value(1) #turn the led off
		

while True:
	blynk.run()
	



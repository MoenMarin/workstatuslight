#!/usr/bin/env python3

import colorsys
import math
import time
import random
from unicornhatmini import UnicornHATMini

uh = UnicornHATMini()
uh.set_brightness(0.5)
map = {"red": 0, "green": 0, "blue": 0}
k = {"red":0, "green": 0, "blue": 0 }
def rgb(i, color):
	if i <= 164 and color == "blue":
		map["blue"] +=  1
	if i >= 131 and i <=247 and color == "green":
		map["green"] += 1
	if i >= 244 and i <= 255 and color == "red":
		map["red"] += 1
def rgbDistribution():
	
	totalValues = map.get("red")+map.get("green")+map.get("blue")
	k["red"] = math.ceil((map.get("red")/totalValues)*119)
	print(k["red"])
	k["green"] = math.ceil((map.get("green")/totalValues)*119)
	k["blue"] =  math.ceil((map.get("blue")/totalValues)*119)
	k["blue"] -= (k["blue"]+k["green"]+k["red"])-(119) 

i=0

try:
	while i<10:

		i+=1
		for y in range(17):
			blue = random.randint(0,255)
			green = random.randint(0,255)
			red = random.randint(0,255)
			rgb(blue, "blue")
			rgb(green, "green")
			rgb(red, "red")
			uh.set_pixel(y,random.randint(0,6), red, green, blue)
			uh.show()
			time.sleep(0.001)
			uh.clear()
			print(map)
	
	uh.clear()
	rgbDistribution()
	print(map)
	print(k)
	while True:
		
		for x in range(7):
			for y in range(17):
				
				
				if k.get("red")!=0:
					print("red")
					k["red"]-=1
					uh.set_pixel(y,x, 255, 0, 0)
				elif k.get("green")!=0:
					k["green"]-=1
					uh.set_pixel(y,x,0,255,0)
				elif k.get("blue")!=0:
					k["blue"]-=1
					uh.set_pixel(y,x,0,0,255)

				uh.show()				
	print(rgbDistribution(map))
	
except KeyboardInterrupt:
	print("done")
	pass

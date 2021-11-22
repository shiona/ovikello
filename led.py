
import math
import time
from rpi_ws281x import Adafruit_NeoPixel, Color

import logging

class Led():

	BLACK = Color(0, 0, 0)
	RED   = Color(255, 0, 0)

	def __init__(self, led_pin, led_count):
		LED_FREQ_HZ = 800000
		LED_DMA = 10
		LED_INVERT = False
		LED_BRIGHTNESS = 255

		self.led_count = led_count
		self.BLINK_FREQ = 1
		self.BLINK_TIME = 10

		logging.debug("setting up %d led(s) on pin %d", self.led_count, led_pin)
		self.strip = Adafruit_NeoPixel(self.led_count, led_pin, LED_FREQ_HZ,
	                                       LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		self.strip.begin()

		self.set_color(self.BLACK)

	def set_color(self, color):
		for i in range(self.led_count):
			self.strip.setPixelColor(i, color)
		self.strip.show()


	def alert(self):
		blink_sleep_time = 1/(2*self.BLINK_FREQ)
		logging.info("led alert!")
		for c in range(math.ceil(self.BLINK_TIME/self.BLINK_FREQ)):
			self.set_color(self.RED)
			time.sleep(blink_sleep_time)

			self.set_color(self.BLACK)
			time.sleep(blink_sleep_time)

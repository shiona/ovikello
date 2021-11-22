
import math
import time
from rpi_ws281x import Adafruit_NeoPixel, Color

import logging

class Led():
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

	def alert(self):
		blink_sleep_time = 1/(2*self.BLINK_FREQ)
		logging.info("led alert!")
		for c in range(math.ceil(self.BLINK_TIME/self.BLINK_FREQ)):

			for i in range(self.led_count):
				self.strip.setPixelColor(i, Color(255, 0, 0))
			self.strip.show()
			time.sleep(blink_sleep_time)

			for i in range(self.led_count):
				self.strip.setPixelColor(i, Color(0, 0, 0))
			self.strip.show()
			time.sleep(blink_sleep_time)


import logging
import math
import time

from rpi_ws281x import Adafruit_NeoPixel, Color

BLACK = Color(0, 0, 0)
RED   = Color(255, 0, 0)

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_INVERT = False
LED_BRIGHTNESS = 255

BLINK_FREQ = 1
BLINK_TIME = 10

class Led():

    def __init__(self, led_pin, led_count):

        self.led_count = led_count

        logging.debug("setting up %d led(s) on pin %d", self.led_count, led_pin)
        self.strip = Adafruit_NeoPixel(self.led_count, led_pin, LED_FREQ_HZ,
                LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()

        self.set_color(BLACK)

    def set_color(self, color):
        for i in range(self.led_count):
            self.strip.setPixelColor(i, color)
        self.strip.show()


    def alert(self):
        blink_sleep_time = 1/(2*BLINK_FREQ)
        logging.info("led alert!")
        for _ in range(math.ceil(BLINK_TIME/BLINK_FREQ)):
            self.set_color(RED)
            time.sleep(blink_sleep_time)

            self.set_color(BLACK)
            time.sleep(blink_sleep_time)

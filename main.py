import bot
import config
import led

import logging

def main():
	logging.basicConfig(level=10)
	logging.debug("Starting, setting up leds")
	ledstrip = led.Led(config.led_pin, config.led_count)
	logging.debug("Leds done, setting up tg bot")
	tgbot = bot.DoorbellBot(config.telegram_token, ledstrip)

	logging.info("Setup done, starting bot")
	tgbot.start()

if __name__ == '__main__':
	main()

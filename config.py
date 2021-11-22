import configparser

_c = configparser.ConfigParser()
_c.read('config.txt')
_c = _c['DEFAULT']

telegram_token = _c.get('telegram_token')

led_count = _c.getint('led_count')
led_pin = _c.getint('led_pin')

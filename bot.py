from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

class DoorbellBot():

	def __init__(self, token, led):
		led = led
		EMOJI_DOOR = "\uD83D\uDEAA"
		DOOR_CALLBACK_DATA = "sesam"

		self.updater = Updater(token=token, use_context=True)
		dispatcher = self.updater.dispatcher

		keyboard = [[ InlineKeyboardButton(EMOJI_DOOR, callback_data=DOOR_CALLBACK_DATA) ]]
		keyboard_markup = InlineKeyboardMarkup(keyboard)

		def start(update, context):
			update.message.reply_text("Mo", reply_markup=keyboard_markup)
	
		def button(update, context):
			query = update.callback_query
			query.answer()

			data = query.data

			if data == DOOR_CALLBACK_DATA:
				led.alert()

		start_handler = CommandHandler("start", start)
		dispatcher.add_handler(start_handler)
		dispatcher.add_handler(CallbackQueryHandler(button))

	def start(self):
		self.updater.start_polling()

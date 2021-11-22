from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

CHECKMARK = '\u2713'

class DoorbellBot():

	def __init__(self, token, led):
		self.updater = Updater(token=token, use_context=True)
		dispatcher = self.updater.dispatcher

		def ovikello(update, context):
			update.message.reply_text(CHECKMARK)
			led.alert()

		ovikello_handler = CommandHandler("ovikello", ovikello)
		dispatcher.add_handler(ovikello_handler)

	def start(self):
		self.updater.start_polling()

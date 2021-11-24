import logging

from telegram.ext import Updater, CommandHandler

import ota


CHECK = '\u2713'
CROSS = '\u2715'
WARNING = '\u26A0'

CONSTRUCTION_SIGN = '\U0001f6a7'

class DoorbellBot():

    def __init__(self, token, led):
        self.create_updater(token)
        dispatcher = self.updater.dispatcher

        def ovikello(update, context):
            update.message.reply_text(CHECK)
            led.alert()

        def upgrade(update, context):
            reply = update.message.reply_text(CONSTRUCTION_SIGN)
            upgrader = ota.OTA()
            try:
                new_version_found = upgrader.run()
                if new_version_found:
                    reply.edit_text(CHECK)
                    self.stop()
                else:
                    reply.edit_text(CROSS)
            except Exception as e:
                logging.warning(e)
                reply.edit_text(WARNING + ' ' + str(e))

        dispatcher.add_handler(CommandHandler("ovikello", ovikello))
        dispatcher.add_handler(CommandHandler("upgrade", upgrade))

    # To be mocked
    def create_updater(self, token):
        self.updater = Updater(token=token, use_context=True)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def stop(self):
        self.updater.stop()

import logging
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
import yaml


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
TOKEN = config['TOKEN']


def start(update: Update, context: CallbackContext):
    text = f"I'm a bot, please talk to me! {update.effective_chat.id}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def check_register_info(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="check_register_info")


def main():
    updater = Updater(token=TOKEN, use_context=True)

    start_handler = CommandHandler(['start', 'test'], start)
    updater.dispatcher.add_handler(start_handler)
    check_register_info_handle = CommandHandler(['check'], check_register_info)
    updater.dispatcher.add_handler(check_register_info_handle)

    updater.start_polling()


if __name__ == "__main__":
    main()

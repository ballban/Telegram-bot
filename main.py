import logging
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot
import yaml


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
TOKEN = config['TOKEN']


updater = Updater(token=TOKEN, use_context=True)
bot = Bot(TOKEN)


def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == 'group':
        text = f'group id: {update.effective_chat.id}'
    else:
        text = f"I'm a bot, please talk to me! {update.effective_chat.id}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def check_register_info(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="check_register_info")


def receive_message(update: Update, context: CallbackContext):
    # here you receive a list of new members (User Objects) in a single service message
    new_members = update.message.new_chat_members
    # do your stuff here:
    for member in new_members:
        print(member.username)


def new_member(update: Update, context: CallbackContext):
    new_members = update.message.new_chat_members
    for member in new_members:
        print(member.id, member.username)


def left_member(update: Update, context: CallbackContext):
    member = update.message.left_chat_member
    print(member.id, member.username)


def test(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=chat_id,
                             text=f'member count: {bot.get_chat_member_count(chat_id)}')
    context.bot.send_message(chat_id=chat_id,
                             text=f'user: {bot.get_chat_member(chat_id, user_id)}')


def main():
    # start message
    start_handler = CommandHandler(['start'], start)
    updater.dispatcher.add_handler(start_handler)
    # check message
    check_register_info_handler = CommandHandler(['check'], check_register_info)
    updater.dispatcher.add_handler(check_register_info_handler)
    # test
    test_handle = CommandHandler(['test'], test)
    updater.dispatcher.add_handler(test_handle)
    # message handler
    new_chat_member_message_handler = MessageHandler(Filters.status_update.new_chat_members, new_member)
    updater.dispatcher.add_handler(new_chat_member_message_handler)
    left_chat_member_message_handler = MessageHandler(Filters.status_update.left_chat_member, left_member)
    updater.dispatcher.add_handler(left_chat_member_message_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()

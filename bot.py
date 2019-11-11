#!/usr/bin/env python3

import re
import logging
from lib.config import config
from lib.todo_handler import todo_handler
from lib.authorization import authorization
from lib.bot_utils import bot_utils
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.parsemode import ParseMode
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from time import sleep
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = config()
handler = todo_handler()
auth = authorization()
bot_utils = bot_utils()

def start_handler(bot, update):
    bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    if not auth.is_authorized(update.message.chat_id):
        unauthorized_user(bot, update)
        return
    bot_utils.send_and_delete(bot, update.message.chat_id, text="\U0001F60A Welcome")

def info_handler(bot, update):
    bot_utils.delete_message(bot, update.message.chat_id, update.message.message_id)
    bot_utils.send_and_delete(bot, update.message.chat_id,
            text="This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram_todo_bot")

def list_handler(bot, update):
    bot_utils.delete_message(bot, update.message.chat_id, update.message.message_id)
    logger.log(msg='list command from user %s' % update.message.chat_id, level=logging.INFO)
    if auth.is_authorized(update.message.chat_id):
        todos = handler.get_todos(update.message.chat_id)
        if  todos == {}:
            bot_utils.send_and_delete(bot, update.message.chat_id, '\U0000274C User %s has no TODO' % update.message.chat_id)
        else:
            for todo in todos: # TODO: strike the todo that are done
                markup = bot_utils.done_menu(todo) if todos[todo]['done'] == 1 else bot_utils.todo_menu(todo)
                message = todos[todo]['description'] if todos[todo]['done'] == 0 else "\U00002705 %s" % (todos[todo]['description'])
                bot_utils.send_and_delete(bot, update.message.chat_id, message, reply_markup=markup)
    else:
        bot_utils.unauthorized_user(bot, update)

def add_user_handler(bot, update):
    bot_utils.delete_message(bot, update.message.chat_id, update.message.message_id)
    message = bot_utils.add_user(bot, update)
    bot_utils.send_and_delete(bot, message['chat_id'], message['text'])

def remove_user_handler(bot, update):
    bot_utils.delete_message(bot, update.message.chat_id, update.message.message_id)
    message = bot_utils.remove_user(bot, update)
    bot_utils.send_and_delete(bot, message['chat_id'], message['text'])

def button(bot, update):
    bot_utils.parse_callback_data(bot, update)

def new_handler(bot, update):
    bot_utils.delete_message(bot, update.message.chat_id, update.message.message_id)
    message = bot_utils.add_todo(bot, update)
    bot_utils.send_and_delete(bot, message['chat_id'], message['text'])

if __name__ == "__main__":
    token = config.get_bot_api()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('list', list_handler))
    dispatcher.add_handler(CommandHandler('info', info_handler))
    dispatcher.add_handler(CommandHandler('new', new_handler))
    dispatcher.add_handler(CommandHandler('add_user', add_user_handler))
    dispatcher.add_handler(CommandHandler('remove_user', remove_user_handler))
    dispatcher.add_handler(CallbackQueryHandler(button, pass_groups=True))
    updater.start_polling(clean=True)


#!/usr/bin/env python3

import re
import logging
from lib.config import config
from lib.todo_handler import todo_handler
from lib.authorization import authorization
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.parsemode import ParseMode
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = config()
handler = todo_handler()
auth = authorization()

def todo_menu(key):
    done = InlineKeyboardButton(text="Done",callback_data="done_%s" % key)
    download = InlineKeyboardButton(text="Delete",callback_data="delete_%s" % key)
    return InlineKeyboardMarkup([[done, download]])

def send_message(bot, chat_id, text, reply_markup=None):
    bot.send_message(chat_id=chat_id, text=text,
            disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def unauthorized_user(bot, update):
    send_message(bot, update.message.chat.id,
            text="\U0001F6AB This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram\_todo\_bot")

def info_handler(bot, update):
    send_message(bot, update.message.chat.id,
            text="This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram\_todo\_bot")

def list_handler(bot, update):
    print('list')
    if auth.is_authorized(update.message.from_user.id):
        todos = handler.get_todos(update.message.from_user.id)
        if  todos == {}:
            send_message(bot, update.message.chat.id, '\U0000274C User %s has no TODO' % update.message.from_user.id)
        else:
            for todo in todos: # TODO: strike the todo that are done
                markup = todo_menu(todo)
                update.message.reply_text(todos[todo]['description'], reply_markup=markup)
    else:
        unauthorized_user(bot, update)

def button(bot, update):
    callback = update.callback_query
    parse_callback_data(bot, update, callback)

def delete_todo(user, key):
    # TODO check if todo still exists and delete it
    ...


def parse_callback_data(bot, update, callback):
    data = callback.data
    if 'done' == data[:4]:
        data = re.sub("done_", '', data)
        # TODO: set todo to done
    if 'delete' == data[:6]:
        data = re.sub('delete_', '', data)
        delete_todo(update.message.from_user.id, data)

if __name__ == "__main__":
    token = config.get_bot_api()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.document, document_handler))
    dispatcher.add_handler(CommandHandler('list', list_handler))
    dispatcher.add_handler(CommandHandler('info', info_handler))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling(clean=True)


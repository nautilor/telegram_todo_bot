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

def delete_message(bot, chat_id, message_id):
    bot.delete_message(chat_id=chat_id, message_id=message_id)

def done_menu(key):
    delete = InlineKeyboardButton(text="\U00002716 Delete", callback_data="delete_%s" % key)
    return InlineKeyboardMarkup([[delete]])

def todo_menu(key):
    done = InlineKeyboardButton(text="\U00002714 Done",callback_data="done_%s" % key)
    delete = InlineKeyboardButton(text="\U00002716 Delete",callback_data="delete_%s" % key)
    return InlineKeyboardMarkup([[done, delete]])

def send_message(bot, chat_id, text, reply_markup=None):
    bot.send_message(chat_id=chat_id, text=text,
            disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def missing_todo(bot, update):
    send_message(bot, update.message.chat.id, text="\U0000274C No text provided \U0000274C")

def unauthorized_user(bot, update):
    send_message(bot, update.message.chat.id,
            text="\U0001F6AB This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram\_todo\_bot")

def start_handler(bot, update):
    if not auth.is_authorized(update.message.from_user.id):
        unauthorized_user(bot, update)
    send_message(bot, update.message.chat.id, text="\U0001F60A Welcome")
    bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def info_handler(bot, update):
    send_message(bot, update.message.chat.id,
            text="This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram\_todo\_bot")

def list_handler(bot, update):
    delete_message(bot, update.message.chat.id, update.message.message_id)
    logger.log(msg='list command from user %s' % update.message.from_user.id, level=logging.INFO)
    if auth.is_authorized(update.message.from_user.id):
        todos = handler.get_todos(update.message.from_user.id)
        if  todos == {}:
            send_message(bot, update.message.chat.id, '\U0000274C User %s has no TODO' % update.message.from_user.id)
        else:
            for todo in todos: # TODO: strike the todo that are done
                markup = done_menu(todo) if todos[todo]['done'] == 1 else todo_menu(todo)
                update.message.reply_text(todos[todo]['description'], reply_markup=markup)
    else:
        unauthorized_user(bot, update)

def button(bot, update):
    user_id = update.callback_query.from_user.id
    callback = update.callback_query
    parse_callback_data(bot, user_id, callback)

def new_handler(bot, update):
    logger.log(msg='new todo from user %s' % update.message.from_user.id, level=logging.INFO)
    if auth.is_authorized(update.message.from_user.id):
        todo = update.message.text
        if (todo == '/new'):
            missing_todo(bot, update)
        else:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            handler.add_todo(update.message.from_user.id, todo.replace('/new ', ''))
            send_message(bot, update.message.chat_id, "\U00002705 Todo created succesfully")
    else:
        unauthorized_user(bot, update)

def delete_todo(user, key):
    logger.log(msg='deleted message %s from user %s' % (key, user), level=logging.INFO)
    handler.delete_todo(user, key)

def done_todo(user, key):
     logger.log(msg='done message %s from user %s' % (key, user), level=logging.INFO)
     handler.complete_todo(user, key)

def parse_callback_data(bot, user, callback):
    data = callback.data
    if 'done' == data[:4]:
        data = re.sub("done_", '', data)
        bot.edit_message_reply_markup(chat_id=callback.message.chat_id,
                message_id=callback.message.message_id, reply_markup=done_menu(data))
        done_todo(user, data)


    if 'delete' == data[:6]:
        data = re.sub('delete_', '', data)
        bot.delete_message(chat_id=callback.message.chat_id, message_id=callback.message.message_id)
        delete_todo(user, data)

if __name__ == "__main__":
    token = config.get_bot_api()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('list', list_handler))
    dispatcher.add_handler(CommandHandler('info', info_handler))
    dispatcher.add_handler(CommandHandler('new', new_handler))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling(clean=True)


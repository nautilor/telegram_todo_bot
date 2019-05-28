#!/usr/bin/env python3

import re
import logging
from .authorization import authorization
from .todo_handler import todo_handler
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.parsemode import ParseMode
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from time import sleep
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class bot_utils:
    def __init__(self):
        self.authorization = authorization();
        self.handler = todo_handler();
    
    def delete_message(self, bot, chat_id, message_id, timeout=0):
        sleep(timeout)
        bot.delete_message(chat_id=chat_id, message_id=message_id)

    def done_menu(self, key):
        delete = InlineKeyboardButton(text="\U00002716 Delete", callback_data="delete_%s" % key)
        return InlineKeyboardMarkup([[delete]])

    def todo_menu(self, key):
        done = InlineKeyboardButton(text="\U00002714 Done",callback_data="done_%s" % key)
        delete = InlineKeyboardButton(text="\U00002716 Delete",callback_data="delete_%s" % key)
        return InlineKeyboardMarkup([[done, delete]])

    def send_and_delete(self, bot, chat_id, text, reply_markup=None, timeout=900): # 2700 = 45min
        message = self.send_message(bot, chat_id, text, reply_markup)
        thread = threading.Thread(target=self.delete_message, args=(bot, chat_id, message.message_id, timeout))
        thread.start()
    
    def send_message(self, bot, chat_id, text, reply_markup=None):
        return bot.send_message(chat_id=chat_id, text=text,
                disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    def missing_todo(self, bot, update):
        self.send_and_delete(bot, update.message.chat.id, text="\U0000274C No text provided \U0000274C")

    def unauthorized_user(self, bot, update):
        self.send_and_delete(bot, update.message.chat.id,
                text="\U0001F6AB This is a personal bot, for more info visit\nhttps://github.com/nautilor/telegram\_todo\_bot")
    
    def delete_todo(self, user, key):
        logger.log(msg='deleted message %s from user %s' % (key, user), level=logging.INFO)
        self.handler.delete_todo(user, key)

    def done_todo(self, user, key):
         logger.log(msg='done message %s from user %s' % (key, user), level=logging.INFO)
         self.handler.complete_todo(user, key)

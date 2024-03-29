#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import queue
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3
import time

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def command(update, context):
    command = update.message.text.split(" ")
    if len(command) > 1:
        logging.info("Bot    : command recived: " + command[1])
        globalMonitorQueue.put(command[1])
        response = globalBotQueue.get()
        update.message.reply_text(response)

def getState(id):
    con=sqlite3.connect('/home/pi/sensordata.db')
    cur = con.cursor()
    cur.execute('SELECT '+ id +' FROM dhtreadings ORDER BY id DESC LIMIT 1')
    result = cur.fetchall()
    return result[0][0]

def temperatura(update, context):
    id = "temperature"
    result = getState(id)
    update.message.reply_text("Temperatura: " + str(result) +" Cº")

def graficoTemperatura(update, context):
    update.message.reply_photo(photo='/home/pi/littleGreen/image.png')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s"', update, context.error)

def startBot(monitorQueue, botQueue):
    global globalMonitorQueue
    globalMonitorQueue = monitorQueue
    print(globalMonitorQueue)

    global globalBotQueue
    globalBotQueue = botQueue
    print(globalBotQueue)
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    f=open("/home/pi/GreenHouse/secret.key", "r")
    key = f.readline().rstrip()
    print(key)
    updater = Updater(key, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("command", command))
    dp.add_handler(CommandHandler("temperatura", temperatura))
    dp.add_handler(CommandHandler("graficoTemp", graficoTemperatura))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()
    while True:
        time.sleep(30)

if __name__ == '__main__':
    startBot(queue.Queue(),queue.Queue() )

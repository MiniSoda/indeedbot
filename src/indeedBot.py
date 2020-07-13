import os
import logging
from datetime import time
from datetime import timezone

import telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Updater

import spiderCtl

spider_server = '192.168.199.151:6800'

def init():
    #admin_id = '206844774'
    id = os.getenv('TELE_ADMIN_ID')
    admin_id = id
    #token = '1099508397:AAGS-2gYoOa_MrKrc4Npa4SHbvPthIR4A1E'
    token = os.getenv('TELE_BOT_TOKEN')

    updater = Updater(token=token, use_context=True)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    job = updater.job_queue
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('show overall info of bot', info)
    dispatcher.add_handler(start_handler)

    job_scrape = job.run_daily(callback_scrape, time(2,0,0,0, timezone(8)))
    job_post = job.run_daily(callback_post, time(9,30,0,0, timezone(8)))
    return updater

def info(update, context):
    #spider and post schedule
    #url list
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def callback_scrape(context: telegram.ext.CallbackContext):
    status, content = spiderCtl.spider_run(spider_server)
    if status != 200 :
        context.bot.send_message(chat_id=admin_id, text='spider error: ' + content)
        

def callback_post(context: telegram.ext.CallbackContext):
    print('one minute!')
    #context.bot.send_message(chat_id='206844774', text='One message every minute')


def main():
    updater = init()
    updater.start_polling()


def if __name__ == "__main__":
    main()




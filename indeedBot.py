import logging
import telegram.ext
import os
from telegram.ext import CommandHandler
from telegram.ext import Updater
import spiderCtl
from datetime import time
from datetime import timezone

id = os.getenv('ADMINID')
token = os.getenv('TOKEN')
spider_server = '192.168.199.151:6800'
admin_id = '206844774'
token = '1099508397:AAGS-2gYoOa_MrKrc4Npa4SHbvPthIR4A1E'

updater = Updater(token=token, use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
job = updater.job_queue
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

job_scrape = job.run_daily(callback_scrape, time(2,0,0,0, timezone(8)))
job_post = job.run_daily(callback_post, time(9,30,0,0, timezone(8)))

updater.start_polling()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def callback_scrape(context: telegram.ext.CallbackContext):
    status, content = spiderCtl.spider_run(spider_server)
    if status != 200 :
        context.bot.send_message(chat_id=admin_id, text='spider error: ' + content)
        

def callback_post(context: telegram.ext.CallbackContext):
    print('one minute!')
    #context.bot.send_message(chat_id='206844774', text='One message every minute')






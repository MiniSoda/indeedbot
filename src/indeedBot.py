import os
import json
import logging
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone

import telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Updater

from content import content_manager
from database import database_manager
import spider

class telegram_bot():
    def __init__(self, database_settings):
        self.database = database_manager(database_settings)
        self.content_manager = content_manager(self.database)
        self.spider_server = database_settings['SPIDER_SERVER']

    def telegram_init(self):
        self.admin_id = os.getenv('TELE_ADMIN_ID')
        self.token = os.getenv('TELE_BOT_TOKEN')
        self.admin_id = 206844774
        self.token = '1099508397:AAGS-2gYoOa_MrKrc4Npa4SHbvPthIR4A1E'

        """
        REQUEST_KWARGS={
            # "USERNAME:PASSWORD@" is optional, if you need authentication:
            'proxy_url': 'http://10.100.0.195:8118/',
        }
        self.updater = Updater(token=self.token, request_kwargs=REQUEST_KWARGS, use_context=True)
        """
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.job = self.updater.job_queue
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('info', self.info)
        dispatcher.add_handler(start_handler)

        start_handler = CommandHandler('pull', self.manual_publish)
        dispatcher.add_handler(start_handler)

        scrawler_hour, scrawler_min = self.database.get_scrawler_schedule()
        publish_hour, publish_min = self.database.get_publish_schedule()

        target_tzinfo = timezone(timedelta(hours=8))
        scrawler_time = datetime.time(hour=scrawler_hour, minute = scrawler_min).replace(tzinfo=target_tzinfo)
        publish_time = datetime.time(hour=publish_hour, minute = publish_min).replace(tzinfo=target_tzinfo)
        
        self.job.run_daily(self.callback_scrape, scrawler_time)
        self.job.run_daily(self.callback_publish, publish_time)
    
    def info(self, update, context):
        clock = datetime.now()
        if update.effective_chat.id != self.admin_id:
            message = "I'm a job hunting bot, please don't talk to me unless you are admin! , it's " + clock.strftime("%H:%M:%S")
        else:
            message = "Hi MiniSoda, it's " + clock.strftime("%H:%M:%S") + "\n[inline URL](http://www.example.com)"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
    def manual_publish(self, update, context):
        try:
            for job_id, job_detail in self.content_manager.publish_content().items():
                context.bot.send_message(chat_id=self.admin_id, text=job_detail, parse_mode=telegram.ParseMode.MARKDOWN_V2)
        except TelegramError.BadRequest(message):
            print(message)

    def callback_scrape(self, context: telegram.ext.CallbackContext):
        status, content = spider.spider_run(self.spider_server)
        if status != 200 :
            context.bot.send_message(chat_id=self.admin_id, text='spider error: ' + content, parse_mode=telegram.ParseMode.MARKDOWN_V2)
        else:
            print('spider spawned')

    def callback_publish(self, context: telegram.ext.CallbackContext):
        for job_id, job_detail in self.content_manager.publish_content().items():
            context.bot.send_message(chat_id=self.admin_id, text=job_detail, parse_mode=telegram.ParseMode.MARKDOWN_V2)
    
    def run(self):
        self.updater.start_polling()

def main():
    with open('src/database.json', 'r') as f:
        settings = json.load(f)
    bot = telegram_bot(settings)
    bot.telegram_init()
    bot.run()

if __name__ == "__main__":
    main()
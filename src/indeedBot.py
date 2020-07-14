import os
import json
import logging
from datetime import time
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

        self.updater = Updater(token=self.token, use_context=True)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        job = self.updater.job_queue
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('info', self.info)
        dispatcher.add_handler(start_handler)

        scrawler_time = self.database.get_scrawler_schedule()
        scrawler_hour = int(scrawler_time[:2])
        scrawler_min = int(scrawler_time[2:])

        publish_time = self.database.get_publish_schedule()
        publish_hour = int(publish_time[:2])
        publish_min = int(publish_time[2:])

        job_scrape = job.run_daily(self.callback_scrape, time(scrawler_hour,scrawler_min,0,0))
        job_post = job.run_daily(self.callback_publish, time(publish_hour,publish_min,0,0))
    
    def info(self, update, context):
        if update.effective_chat.id != self.admin_id:
            message = "I'm job hunting bot, please don't talk to me unless you are admin!"
        else:
            message = "Hi MiniSoda"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    def callback_scrape(self, context: telegram.ext.CallbackContext):
        status, content = spider.spider_run(self.spider_server)
        if status != 200 :
            context.bot.send_message(chat_id=self.admin_id, text='spider error: ' + content)

    def callback_publish(self, context: telegram.ext.CallbackContext):
        for job_id, job_detail in self.content_manager.publish_content():
            context.bot.send_message(chat_id=self.admin_id, text=job_detail)
    
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
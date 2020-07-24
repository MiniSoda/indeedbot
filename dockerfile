#
# Dockerfile for telegram-bot-deploy
#

FROM debian:buster
LABEL maintainer="https://github.com/MiniSoda"

RUN set -xe \
    && apt-get update \
    && apt-get install -y git \
						  python3 \
                          python3-pip \
    && git clone https://github.com/MiniSoda/indeedbot.git \
    && pip install python-telegram-bot\
				   pymongo \ 
    && rm -rf /var/lib/apt/lists/*

VOLUME /etc/telebot/

CMD ["python3", "indeedbot/src/indeedBot.py"]
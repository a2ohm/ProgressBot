#! /usr/bin/python3
# -*- coding:utf-8 -*-

# by antoine@2ohm.fr

import sys
import time
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("\tchat_id: {}".format(chat_id))

    if content_type == 'text' and msg['text'] == '/start':
        ans = """
Hello <b>{first_name}</b>, nice to meet you!\n
Your chat_id is <code>{chat_id}</code>.\n
You can stop the <code>get_chat_id</code> script with <code>CTRL+C</code> and start using the ProgressBot right now.\n
See you soon!
        """.format(first_name = msg['from']['first_name'],
                   chat_id = chat_id)
        
        bot.sendMessage(chat_id, ans, parse_mode = "HTML")

TOKEN = "PUT_YOUR_TOKKEN_HERE"

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print()
        sys.exit()

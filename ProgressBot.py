#! /usr/bin/python3
# -*- coding:utf-8 -*-

import telepot
import traceback
from datetime import datetime, timedelta

class ProgressBot:
    def __init__(self, task = "", updates = (0.1, 60)):

        """Init the bot."""

        # Load the config file
        self.loadConfig()

        # Save parameters
        self.task = task
        self.update_percent_rate = updates[0]
        self.update_time_rate = updates[1]

        # Create the bot
        self.bot = telepot.Bot(self.token)

        # Create intern flags
        self.F_pause = False
        #   F_silentMode: stay silent until the first tick. This is a
        #                 trick to ignore commands send between two
        #                 runs.
        self.F_silentMode = True
        #   F_mute: turn it on to mute tick reports.
        self.F_mute = False

    def __enter__(self):
        msg = "Hello, I am looking on a new task: <b>{task}</b>.".format(
                task = self.task)
        self.sendMessage(msg)

        # Init the progress status
        self.progress = 0
        self.start_time = datetime.now()
        self.last_percent_update = 0
        self.last_time_update = self.start_time

        # Start the message loop
        # note: incoming message will be ignore until the first tick
        #       (in order to flush messages sent between two tasks)
        self.bot.message_loop(self.handle)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is KeyboardInterrupt:
            msg = "The task <b>{task}</b> was interrupted.".format(
                    task = self.task)
        else:
            msg = "The task <b>{task}</b> is complete.".format(
                    task = self.task)

        self.sendMessage(msg)
        return True

    def loadConfig(self):
        with open('./ProgressBot.cfg', 'r') as f:
            for line in f.readlines():
                if line[0] == '#':
                    continue

                parsed_line = line.split('=')
                if parsed_line[0] == 'token':
                    if len(parsed_line) == 2:
                        self.token = parsed_line[1].strip()
                    else:
                        raise ValueError("Please provide a valid tokken in ProgressBot.cfg")

                if parsed_line[0] == 'chat_id':
                    if len(parsed_line) == 2:
                        self.chat_id = parsed_line[1].strip()
                    else:
                        # If the chat_id is empty, maybe it is because
                        # it is still unknown.
                        print("Hello, you didn't provide any chat_id. Maybe you do not know it. The get_chat_id in the tools directory may help you with this issue.")

                        raise ValueError("You have to provide a valid chat_id, use the get_chat_id script to get help with that.")


    def sendMessage(self, msg):
        self.bot.sendMessage(self.chat_id, msg, parse_mode = "HTML")

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if not self.F_silentMode and content_type == 'text':
            if msg['text'] == '/pause':
                print("Task: pause")
                self.F_pause = True
                self.send_status(cmt = "pause")
            elif msg['text'] == '/resume':
                print("Task: resume")
                self.F_pause = False
                self.send_status(cmt = "resume")
            elif msg['text'] == '/status':
                self.send_status()
            elif msg['text'] == '/mute':
                self.F_mute = True
            elif msg['text'] == '/unmute':
                self.F_mute = False

# API

    def info(self, msg):
        self.sendMessage(msg)

    def tick(self, progress):
        # Turn off the silentMode
        self.F_silentMode = False

        # Update the progress
        self.progress = progress

        # Freeze if paused
        while self.F_pause:
            time.sleep(1)

        # Check if a progress update is necessary based on progress
        if self.progress - self.last_percent_update >= self.update_percent_rate:
            self.send_status()

        # Check if a progress update is necessary based on time ellapsed
        if datetime.now() - self.last_time_update >= timedelta(seconds=self.update_time_rate):
            self.send_status()

    def send_status(self, cmt = "", force = False):
        """Send the current status of the task."""
        # Return without sending anything if mute
        if self.F_mute and not force:
            return

        # Send the current status
        if cmt:
            msg = "{timestamp} − {progress:3.0f}% ({cmt})".format(
                    timestamp = datetime.now().strftime('%H:%M:%S'),
                    progress = 100*self.progress,
                    cmt = cmt)
        else:
            msg = "{timestamp} − {progress:3.0f}%".format(
                    timestamp = datetime.now().strftime('%H:%M:%S'),
                    progress = 100*self.progress)

        self.sendMessage(msg)

        # Update progress status
        self.last_percent_update = self.progress
        self.last_time_update = datetime.now()

if __name__ == '__main__':
    # Demo of ProgressBot
    import time

    task= "Example"
    with ProgressBot(task, updates = (0.2, 60)) as pbot:
        for i in range(10):
            time.sleep(1)
            pbot.tick(progress = i/10)


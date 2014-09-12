import asyncio
import os
import signal
import re
import imp

from toolbot.adapter.shell import ShellAdapter
from toolbot.adapter.irc import IrcAdapter
from toolbot.brain import Brain
from toolbot.httpd import start_server
from toolbot.listener import Listener, TextListener
from toolbot.message import (
    EnterMessage,
    LeaveMessage,
    TopicMessage,
    CatchAllMessage
)


class Robot:
    def __init__(self, name="toolbot"):
        self.name = name
        self.adapter = IrcAdapter(self)
        #self.adapter = ShellAdapter(self)
        self.brain = Brain(self)
        self.listeners = []
        self.httpd = None
        self.loop = None

    def hear(self, regex):
        def hear_decorator(callback):
            self.listeners.append(TextListener(self, regex, callback))
            return callback
        return hear_decorator

    def respond(self, regex):
        def respond_decorator(callback):
            name = self.name
            new_re = re.compile("^@?{}[:,]?\\s*(?:{})".format(name, regex))
            self.listeners.append(TextListener(self, new_re, callback))
            return callback
        return respond_decorator

    def enter(self):
        def enter_decorator(callback):
            self.listeners.append(
                Listener(self,
                         lambda msg: isinstance(msg, EnterMessage),
                         callback)
            )
            return callback
        return enter_decorator

    def leave(self):
        def leave_decorator(callback):
            self.listeners.append(
                Listener(self,
                         lambda msg: isinstance(msg, LeaveMessage),
                         callback)
            )
            return callback
        return leave_decorator

    def topic(self):
        def topic_decorator(callback):
            self.listeners.append(
                Listener(self,
                         lambda msg: isinstance(msg, TopicMessage),
                         callback)
            )
            return callback
        return topic_decorator

    def error(self, callback):
        ...

    def catchAll(self):
        def catchAll_decorator(callback):
            self.listeners.append(
                Listener(self,
                         lambda msg: isinstance(msg, CatchAllMessage),
                         callback)
            )
            return callback
        return catchAll_decorator

    def receive(self, message):
        results = []
        for listener in self.listeners:
            results.append(listener(message))
            if message.done:
                break
        if not isinstance(message, CatchAllMessage) and not any(results):
            self.receive(CatchAllMessage(message))

    def send(self, user, *strings):
        self.adapter.send(user, *strings)

    def reply(self, user, *strings):
        self.adapter.reply(user, *strings)

    def messageRoom(self, room, *strings):
        envelope = {"room": room}
        self.adapter.send(envelope, *strings)

    def sigint(self):
        self.adapter.close()
        self.loop.stop()
        exit(0)

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.sigint)

        self.httpd = start_server(self.loop)
        bot.load_scripts()
        self.adapter.run(self.loop)

        self.loop.run_forever()

    def load_scripts(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        scripts_dir = os.path.join(this_dir, 'scripts')

        for fn in os.listdir(scripts_dir):
            if fn.endswith('.py') and not fn.startswith('_'):
                p = os.path.join(scripts_dir, fn)
                m = imp.load_source(fn[:-3], p)
                if hasattr(m, 'plugin'):
                    m.plugin(self)


if __name__ == "__main__":
    bot = Robot()

    bot.run()

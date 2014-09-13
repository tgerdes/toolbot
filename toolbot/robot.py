import asyncio
import os
import signal
import re
import imp

from toolbot.adapter.shell import ShellAdapter
from toolbot.adapter.irc import IrcAdapter
from toolbot.brain import Brain
import toolbot.httpd
from toolbot.listener import Listener, TextListener
from toolbot.message import (
    EnterMessage,
    LeaveMessage,
    TopicMessage,
    CatchAllMessage
)


class Robot:
    def __init__(self, adapterClass, name="toolbot"):
        self.name = name
        self.adapter = adapterClass(self)
        self.brain = Brain(self)
        self.listeners = []
        self.httpd = toolbot.httpd.app
        self.loop = None

    def hear(self, regex):
        def hear_decorator(callback):
            self.listeners.append(TextListener(self, regex, callback))
            return callback
        return hear_decorator

    def respond(self, regex):
        def respond_decorator(callback):
            if isinstance(regex, str):
                r = re.compile(regex)
            else:
                r = regex
            name = self.name
            new_re = re.compile("^@?{}[:,]?\\s*(?:{})".format(name,
                                                              r.pattern),
                                r.flags)
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
            try:
                results.append(listener(message))
            except Exception as e:
                pass
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
        self.stop()
        exit(0)

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.sigint)

        toolbot.httpd.start_server(self.loop)
        self.load_scripts()
        self.adapter.run(self.loop)

        self.loop.run_forever()

    def stop(self):
        self.adapter.close()
        self.loop.stop()

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
    adapterClass = IrcAdapter
    adapterClass = ShellAdapter
    bot = Robot(adapterClass)

    bot.run()

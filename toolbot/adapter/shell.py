import asyncio
import sys

from toolbot.adapter import Adapter
from toolbot.message import TextMessage


class ShellAdapter(Adapter):

    def __init__(self, bot):
        super().__init__(bot)

    def send(self, envelope, *strings):
        for string in strings:
            # TODO: async print?
            print("\x1b[01;32m{}\x1b[0m".format(string))

    def emote(self, envelope, *strings):
        self.send(envelope, *("* {}".format(string) for string in strings))

    def reply(self, envelope, *strings):
        self.send(envelope, *("{name}: {msg}".format(
            name=envelope['user'].name,
            msg=string) for string in strings))

    @asyncio.coroutine
    def input_loop(self, loop):
        f = sys.stdin
        fno = f.fileno()
        q = asyncio.Queue()

        def do_read():
            q.put_nowait(f.readline())

        loop.add_reader(fno, do_read)

        while True:
            print("{}> ".format(self.bot.name), end="")
            sys.stdout.flush()

            line = yield from q.get()

            if not line:
                print()
                break

            user = self.bot.brain.userForId(1, name="Shell", room="Shell")
            self.receive(TextMessage(user, line, "messageId"))

        loop.remove_reader(fno)
        self.bot.loop.stop()

    def run(self, loop):
        asyncio.async(self.input_loop(loop))

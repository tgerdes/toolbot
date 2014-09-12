import irc3

from toolbot.adapter import Adapter
from toolbot.message import (
    TextMessage,
    EnterMessage,
    LeaveMessage,
    TopicMessage)


@irc3.plugin
class Irc3ToToolbot:
    requires = ['irc3.plugins.core', ]

    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def message(self, mask, event, target, data):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        user = bot.brain.userForId(mask, name=mask.nick, room=target)
        adapter.receive(TextMessage(user, data))

    @irc3.event(irc3.rfc.JOIN)
    def join(self, mask, channel):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        if channel.startswith(":"):
            channel = channel[1:]
        user = bot.brain.userForId(mask, name=mask.nick, room=channel)
        adapter.receive(EnterMessage(user))

    @irc3.event(irc3.rfc.PART)
    def part(self, mask, channel, data):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        if channel.startswith(":"):
            channel = channel[1:]
        user = bot.brain.userForId(mask, name=mask.nick, room=channel)
        adapter.receive(LeaveMessage(user, data))

    @irc3.event(irc3.rfc.QUIT)
    def quit(self, mask, data):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        user = bot.brain.userForId(mask, name=mask.nick)
        adapter.receive(LeaveMessage(user, data))

    @irc3.event(r':(?P<mask>\S+) TOPIC (?P<channel>\S+)( :(?P<data>.*)|$)')
    def topic(self, mask, channel, data):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        user = bot.brain.userForId(mask, name=mask.nick, room=channel)
        adapter.receive(TopicMessage(user, data))

    @irc3.event(irc3.rfc.RPL_TOPIC)
    def topic_rpl(self, srv, me, channel, data):
        # TODO: store topic? Wait for RPL_TOPICWHOTIME? also?
        pass

    @irc3.event(r"^:(?P<srv>\S+) 353 (?P<me>\S+) (?P<mode>[@*=]) "
                r"(?P<channel>\S+) :(?P<data>.*)")
    def rpl_namreply(self, srv, me, mode, channel, data):
        names = data.split(" ")
        for name in names:
            if name.startswith('@') or name.startswith('+'):
                name = name[1:]
            # TODO: store names?


class IrcAdapter(Adapter):
    def __init__(self, bot):
        super().__init__(bot)
        self.irc = irc3.IrcBot(
            nick=bot.name,
            autojoins=['#irc3'],
            host='localhost', port=6667, ssl=False,
            includes=[__name__],
            adapter=self)

    def send(self, envelope, *strings):
        for string in strings:
            self.irc.privmsg(envelope['room'], string)

    def emote(self, envelope, *strings):
        self.send(envelope, *("\u0001ACTION {}\u0001".format(string)
                              for string in strings))

    def reply(self, envelope, *strings):
        self.send(envelope, *("{}: {}".format(envelope['user'].name, string)
                              for string in strings))

    def topic(self, envelope, *strings):
        data = ":" + " / ".join(strings)
        channel = envelope['room']
        self.irc.send("TOPIC {} {}".format(channel, data))

    def run(self, loop):
        self.irc.create_connection()

    def close(self):
        if getattr(self.irc, 'protocol'):
            self.irc.quit("quitting")
            self.irc.protocol.transport.close()

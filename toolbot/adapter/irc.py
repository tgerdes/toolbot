import irc3

from toolbot.adapter import Adapter
from toolbot.message import TextMessage

@irc3.plugin
class MyPlugin:
    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
    ]

    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.PRIVMSG)
    def message(self, mask, event, target, data):
        adapter = self.bot.config['adapter']
        bot = adapter.bot
        user = bot.brain.userForId(mask, name=mask.nick, room=target)
        adapter.receive(TextMessage(user, data, "messageId"))


    @irc3.event(irc3.rfc.JOIN)
    def welcome(self, mask, channel):
        """Welcome people who join a channel"""
        if channel.startswith(":"):
            channel = channel[1:]

class IrcAdapter(Adapter):
    def __init__(self, bot):
        super().__init__(bot)
        self.irc = irc3.IrcBot(
            nick=bot.name,
            autojoins=['#irc3'],
            host='localhost', port=6667, ssl=False, 
            includes=[
                "irc3.plugins.core",
                __name__
            ],
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

    #TODO: topic
    #def topic(self, envelope, *strings):
    #    pass

    #def play(self, envelope, *strings):
    #    pass

    def run(self, loop):
        self.irc.run(forever=False)

    def close(self):
        pass

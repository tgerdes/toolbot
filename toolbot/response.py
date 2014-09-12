
class Response:
    def __init__(self, bot, message, match):
        self.bot = bot
        self.message = message
        self.match = match
        self.envelope = {
            "room": message.room,
            "user": message.user,
            "message": message
        }

    def send(self, *strings):
        self.bot.adapter.send(self.envelope, *strings)

    def emote(self, *strings):
        self.bot.adapter.emote(self.envelope, *strings)

    def reply(self, *strings):
        self.bot.adapter.reply(self.envelope, *strings)

    def topic(self, *strings):
        self.bot.adapter.topic(self.envelope, *strings)

    def play(self, *strings):
        self.bot.adapter.play(self.envelope, *strings)

    def locked(self, *strings):
        self.bot.adapter.locked(self.envelope, *strings)

    def finish(self):
        self.message.finish()

class Adapter:
    def __init__(self, bot):
        self.bot = bot

    def send(self, envelope, *strings):
        pass

    def emote(self, envelope, *strings):
        pass

    def reply(self, envelope, *strings):
        pass

    def topic(self, envelope, *strings):
        pass

    def play(self, envelope, *strings):
        pass

    def run(self, loop):
        pass

    def close(self):
        pass

    def receive(self, message):
        self.bot.receive(message)

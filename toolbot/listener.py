import re
from toolbot.message import TextMessage
from toolbot.response import Response


class Listener:
    def __init__(self, bot, matcher, callback):
        self.bot = bot
        self.matcher = matcher
        self.callback = callback

    def __call__(self, message):
        match = self.matcher(message)
        if match:
            self.callback(Response(self.bot, message, match))
            return True
        return False


class TextListener(Listener):
    def __init__(self, bot, regex, callback):
        if isinstance(regex, str):
            regex = re.compile(regex)

        def matcher(message):
            if isinstance(message, TextMessage):
                return message.match(regex)
        super().__init__(bot, matcher, callback)

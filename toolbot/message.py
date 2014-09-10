
class Message:
    def __init__(self, user, text=None, id=None, done=False):
        self.text = text
        self.id = id
        self.user = user
        self.done = done
        self.room = user.room

    def finish(self):
        self.done = True


class TextMessage(Message):
    def match(self, regex):
        return regex.match(self.text)

    def __str__(self):
        return self.text


class EnterMessage(Message):
    pass


class LeaveMessage(Message):
    pass


class TopicMessage(TextMessage):
    pass


class CatchAllMessage(Message):
    def __init__(self, message):
        super().__init__(message.user)
        self.message = message

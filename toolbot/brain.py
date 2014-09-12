from toolbot.user import User


class Brain:
    def __init__(self, bot):
        self.data = {
            'users': {},
            '_private': {},
        }
        self.bot = bot

    def set(self, key, value):
        self.data['_private'][key] = value
        return self

    def get(self, key):
        self.data['_private'].get(key)
        return self

    def remove(self, key):
        del self.data['_private'][key]
        return self

    def save(self):
        ...

    def close(self):
        ...

    def users(self):
        return self.data['users']

    def userForId(self, id, **kwargs):
        if id in self.data['users']:
            user = self.data['users'][id]
        else:
            user = User(id, **kwargs)

        room = kwargs.get('room')
        if room and getattr(user, 'room') != room:
            user = User(id, **kwargs)
            self.data['users'][id] = user

        return user

    def userForName(self, name):
        lower = name.lower()
        for user in self.data['users'].values:
            if lower == getattr(user, 'name', "").lower():
                return user
        return None

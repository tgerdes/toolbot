class User:
    def __init__(self, id, **kwargs):
        self.id = id
        for k, v in kwargs.items():
            setattr(self, k, v)
        if 'name' not in kwargs:
            self.name = self.id

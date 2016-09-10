__all__ = ['StringAttributes', 'field_keys', 'item_keys', 'encoding', 'log']

class StringAttributes():
    def __init__(self, items):
        for i in items:
            setattr(self, i, i)
    def __iter__(self):
        return iter(self.__dict__.keys())

field_keys = StringAttributes([
    'label',
    'referer',
    'folder',
    'headers',
    'postData',
    'cookies',
    'userAgent',
    'items',
])
item_keys = StringAttributes([
    'url',
    'filename'
])
encoding = 'utf-8'
def log(message): print(message)

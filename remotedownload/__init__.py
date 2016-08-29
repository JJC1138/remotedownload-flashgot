__all__ = ['fields', 'encoding', 'log']

class Struct:
	def __init__(self, **entries):
		self.__dict__.update(entries)

fields = Struct(
	comment = 'comment',
	referer = 'referer',
	folder = 'folder',
	filename = 'fname',
	headers = 'headers',
	post = 'post',
	urls = 'ufile',
	cookies_txt = 'cfile',
	userpass = 'userpass',
	user_agent = 'ua',
)
encoding = 'utf-8'
def log(message): print(message)

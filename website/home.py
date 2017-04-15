from website import website

@website.route('/')
@website.route('/index')
def index():
    return "Hello, World!"

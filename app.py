from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


if __name__ == '__main__':
    app.run()

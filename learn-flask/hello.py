from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    copy the following line into browser:
        http://127.0.0.1:5000/
    :return: a string 'Hello, World!'
    """
    return 'Hello, World!  This is the index page,  also known as the root.'


@app.route('/lmc')
def hello_lmc():
    """
    copy the following line into browser:
        http://127.0.0.1:5000/lmc
    :return: a string 'Hello, lmc!'
    """
    return 'Hello, lmc!'


@app.route('/user/<username>')
def show_user_profile(username):
    # 用<>括起来的部分URL 可以作为参数
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 同时指定参数的解释类型为 int
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/  “路径”也是一种内置类型
    return 'Subpath %s' % escape(subpath)

'''
flask接受的类型
string(缺省值)
int
float
path
uuid :UUID字符串
'''

# 定义的时候尾部加了/的URL 在访问时无论你加不加/，flask都会帮你加上/
# 定义的时候没有加/的URL，访问时必须没有/  （因为它就像一个文件）



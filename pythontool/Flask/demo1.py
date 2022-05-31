from flask import Flask, url_for, request, render_template, make_response, redirect

# https://docs.pythontab.com/flask/flask0.10/quickstart.html
app = Flask(__name__)


@app.route('/hello3/<username>', methods=['GET', 'POST'])
def hello_world3(username):
    if request.method == 'POST':
        return 'Hello World3 POST %s!' % username
    else:
        return 'Hello World3 GET %s!' % username


# path的作用是接收/的路径
@app.route('/hello2/<path:username>')
def hello_world2(username):
    return 'Hello World2 %s!' % username


@app.route('/hello1/<int:post_id>')
def hello_world1(post_id):
    return 'Hello World1 %d!' % post_id


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# cookie
@app.route('/')
def index(name=None):
    username = request.cookies.get('username')
    print("cookie %s" % username)
    resp = make_response(render_template('hello.html', name=name))
    resp.set_cookie('username', 'kevin')
    return resp


# 重定向和错误
@app.route('/redirect')
def index1():
    return redirect(url_for('hello'))


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('hello_world3', username='JohnDoe', jj='hhh'))
        print(url_for('static', filename='style.css'))
    app.run(host='0.0.0.0', debug=True)

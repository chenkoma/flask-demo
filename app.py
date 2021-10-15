from flask import Flask, escape, url_for, render_template
from exts import db
import config
from user.index import *
import click

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)
app.register_blueprint(user, url_prefix="/user")


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

# @app.route('/')
# def hello():
#     return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.cli.command()
def forge():
    db.create_all()
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# @app.route('/')
# def index():
#     # name = 'Grey Li'
#     # movies = [
#     #     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     #     {'title': 'Dead Poets Society', 'year': '1989'},
#     #     {'title': 'A Perfect World', 'year': '1993'},
#     #     {'title': 'Leon', 'year': '1994'},
#     #     {'title': 'Mahjong', 'year': '1996'},
#     #     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     #     {'title': 'King of Comedy', 'year': '1999'},
#     #     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     #     {'title': 'WALL-E', 'year': '2008'},
#     #     {'title': 'The Pork of Music', 'year': '2012'},
#     # ]
#     return render_template('index.html', name=name, movies=movies)

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first
    # return render_template('404.html', user=user), 404
    return render_template('404.html'), 404


@app.route('/')
def index():
    user = User.query.first()
    print(user.name)
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


@app.route('/')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields


class User(db.Model, EntityBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model, EntityBase):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/list')
def user_list():
    # users = User.query.all()
    users = Movie.query.all()
    print(users)
    users_output = []
    for user in users:
        users_output.append(user.to_json())
    return jsonify(users_output)


@app.route('/add')
def user_add():
    a = User(name='koma')
    db.session.add(a)
    db.session.commit()
    return jsonify(True)


if __name__ == '__main__':
    app.run(debug=True)

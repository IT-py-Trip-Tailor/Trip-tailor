from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1111'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/')
def index():
    # Проверяем, если пользователь уже вошел, перенаправляем на его аккаунт
    if 'user_id' in request.cookies:
        return redirect('/account')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)

        try:
            db.session.commit()
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            error_message = 'Пользователь с таким логином или почтой уже существует.'
            return render_template('register.html', error_message=error_message)
    return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login_input']
        password = request.form['password']

        user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()

        if user and user.password == password:
            response = make_response(redirect('/account'))
            response.set_cookie('user_id', str(user.id))
            return response

        error_message = 'Неправильное имя пользователя (логин или почта) или пароль.'
        return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/account')
def account():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if not user:
        return redirect('/login')

    return render_template('account.html', username=user.username)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

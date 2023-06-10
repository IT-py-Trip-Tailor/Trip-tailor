from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import sys
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

    
def generate_unique_key():
    # Генерация случайной строки
    cookie_value = secrets.token_hex(16)
    return cookie_value


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    unique_key = db.Column(db.String(16))
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    patronymic = db.Column(db.String(50), nullable=True)
    birth_date = db.Column(db.String(10), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)
    child = db.Column(db.String(50), nullable=True)

# Создание таблицы, если она отсутствует
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Проверка наличия куки с именем пользователя
    cookie = request.cookies.get('unique_key')
    if cookie:
        user = User.query.filter_by(unique_key=cookie).first()
        try:
            user.email
        except:
            return render_template('index.html')
        return render_template('profile.html', user=user)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получение данных из формы регистрации
        username = request.form['login']
        email = request.form['email']
        password = request.form['password']
        unique_key = generate_unique_key()
        # Хэширование пароля
        hashed_password = generate_password_hash(password)
        # Создание нового пользователя
        try:
            user = User.query.filter((User.email == email)).first()
            user.email
            error_message = 'Такая почта уже используется, воспользуйтесь входом'
            return redirect(url_for('login.html', error_message=error_message))
        except:
            new_user = User(username=username, email=email, password=hashed_password, unique_key=unique_key)
            db.session.add(new_user)
            db.session.commit()
            # Перенаправление на страницу входа
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('unique_key', unique_key)
            return resp    

    return render_template('reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получение данных из формы входа
        login = request.form['login']
        password = request.form['password']
        # Поиск пользователя по имени пользователя или адресу электронной почты
        user = User.query.filter((User.username == login) | (User.email == login)).first()
        if user and check_password_hash(user.password, password):
            # Установка куки с именем пользователя
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('unique_key', user.unique_key)
            return resp
        else:
            return render_template('login.html', error_message='Неправильно введен логин или пароль')

    error_message = request.args.get('error_message')
    if error_message == 'not_loginning':
        return render_template('login.html', error_message='Вы не вошли в аккаунт')

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    cookie = request.cookies.get('unique_key')

    if request.method == 'POST':
        try:
            user = User.query.filter(User.unique_key == cookie).first()
            # Получение данных из формы
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            patronymic = request.form.get('patronymic')
            birth_date = request.form.get('birth_date')
            phone_number = request.form.get('phone_number')
            city = request.form.get('city')
            gender = request.form.get('gender')
            marital_status = request.form.get('marital_status')
            child = request.form.get('child')

            # Обновление полей пользователя
            user.first_name = first_name
            user.last_name = last_name
            user.patronymic = patronymic
            user.birth_date = birth_date
            user.phone_number = phone_number
            user.city = city
            user.gender = gender
            user.marital_status = marital_status
            user.child = child

            db.session.commit()
        except:
            return redirect(url_for('login', error_message='not_loginning'))

    # Проверка наличия куки с именем пользователя
    if cookie:
        # Поиск пользователя по имени пользователя
        user = User.query.filter_by(unique_key=cookie).first()
        if user:
            return render_template('profile.html', user=user)
    # Если куки с именем пользователя отсутствуют или пользователь не найден, перенаправляем на страницу входа
    return redirect(url_for('login', error_message='not_loginning'))

@app.route('/all_tour')
def all_tour():
    return render_template('all_tour.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/tour_info')
def tour_info():
    return render_template('tour_info.html')

# Загрузка данных
data = pd.read_csv('tour_data.csv')

# Предобработка данных
le = LabelEncoder()
data['Откуда'] = le.fit_transform(data['Откуда'])
data['Куда'] = le.fit_transform(data['Куда'])
data['Тип тура'] = le.fit_transform(data['Тип тура'])
data['Цель тура'] = le.fit_transform(data['Цель тура'])
data['Трансфер'] = le.fit_transform(data['Трансфер'])
data['Тип размещения'] = le.fit_transform(data['Тип размещения'])
data['Питание'] = le.fit_transform(data['Питание'])
data['Активности'] = le.fit_transform(data['Активности'])
data['Язык гида'] = le.fit_transform(data['Язык гида'])

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)


@app.route('/tour_package', methods=['GET', 'POST'])
def tour_package():
    if request.method == 'POST':
        user_input = {
            'Откуда': request.form.get('from'),
            'Куда': request.form.get('where'),
            'Бюджет': float(request.form.get('cost1')),
            'Тип тура': request.form.get('type_tour'),
            'Цель тура': request.form.get('target'),
            'Трансфер': request.form.get('transfer1'),
        }

        # Преобразование пользовательских данных
        for col, value in user_input.items():
            if col in le.classes_:
                user_input[col] = le.transform([value])[0]

        user_data = scaler.transform(pd.DataFrame([user_input]))

        # KNN алгоритм
        knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
        knn.fit(scaled_data)
        _, indices = knn.kneighbors(user_data)

        # Вывод результатов
        recommended_tours = data.iloc[indices[0]]
        # Преобразование в удобочитаемый формат
        recommended_tours = recommended_tours.to_dict(orient='records')

        return render_template('tour_package.html', tours=recommended_tours)

    return render_template('tour_package.html', tours=[])

if __name__ == '__main__':
    app.run(debug=True)

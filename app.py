from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')
mongo = PyMongo(app)

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'login': request.form['username']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            new_user = {
                'login': request.form['username'],
                'password_cache': hashpass,
                'volumes': [],
                'states': []
            }
            users.insert_one(new_user)
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))

        return render_template('register.html', error=True) # Это имя пользоватея уже занято

    return render_template('register.html', error=False)

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'login': request.form['username']})

        if login_user:
            if check_password_hash(login_user['password_cache'], request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))

        return render_template('login.html', error=True) # Неверное имя пользователя или пароль 

    return render_template('login.html', error=False)

# Выход
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Главная страница
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Панель управления
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        users = mongo.db.users
        volumes = mongo.db.volumes
        states = mongo.db.states
        user_data = users.find_one({'login': session['username']})

        user_volumes = [volumes.find_one({'_id': vol_id}) for vol_id in user_data['volumes']]
        user_states = [states.find_one({'_id': state_id}) for state_id in user_data['states']]
        
        content = {
            state['name']: {
                'volumes': [volume for volume in user_volumes if volume['state'] == state['_id']],
                'state': state
            }
            for state in user_states}
        # content_preview = {key: {'volumes': value['volumes'][:7], 'state': value['state']} for key, value in content.items()}
        
        return render_template(
            'dashboard.html',
            content=content,
            states=user_states
        )
    return redirect(url_for('index'))

# Добавление тома
@app.route('/add_volume', methods=['POST'])
def add_volume():
    if 'username' in session:
        users = mongo.db.users
        volumes = mongo.db.volumes
        states = mongo.db.states
        user_data = users.find_one({'login': session['username']})

        # Создание нового тома
        new_volume = {
            '_id': volumes.count_documents({}),
            'title': request.form.get('title', 'Новый том'),
            'description': request.form.get('description', 'Здесь пока нет описания.'),
            'cover_art_link': request.form.get('cover_art_link', ''),
            'state': int(request.form.get('state', 0))  # Состояние как индекс
        }
        
        volumes.insert_one(new_volume)
        user_data['volumes'].append(new_volume['_id'])
        users.update_one({'login': session['username']}, {'$set': {'volumes': user_data['volumes']}})
        return redirect(url_for('dashboard'))

    return redirect(url_for('index'))

# Редактирование тома
@app.route('/edit_volume/<int:volume_id>', methods=['POST'])
def edit_volume(volume_id):
    if 'username' in session:
        volumes = mongo.db.volumes
        volume = volumes.find_one({'_id': volume_id})

        if volume:
            update_data = {
                'title': request.form.get('title', volume['title']),
                'description': request.form.get('description', volume['description']),
                'cover_art_link': request.form.get('cover_art_link', volume['cover_art_link']),
                'state': int(request.form.get('state', volume['state']))  # Индекс состояния
            }

            volumes.update_one({'_id': volume_id}, {'$set': update_data})
            return redirect(url_for('dashboard'))

    return redirect(url_for('index'))

@app.route('/delete_volume/<int:volume_id>', methods=['POST'])
def delete_volume(volume_id):
    if 'username' in session:
        users = mongo.db.users
        user_data = users.find_one({'login': session['username']})
        
        if (volume_id in user_data['volumes']):
            del user_data['volumes'][user_data['volumes'].index(volume_id)]
        
        users.update_one({'login': session['username']}, {'$set': user_data})
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('index'))

@app.route('/edit_state/<int:state_id>', methods=['POST'])
def edit_state(state_id):
    if 'username' in session:
        states = mongo.db.states
        state = states.find_one({'_id': state_id})

        if state:
            update_data = {
                'name': request.form.get('name', state['name']),
                'color': request.form.get('color', state['color'])
            }

            states.update_one({'_id': state_id}, {'$set': update_data})
            return redirect(url_for('dashboard'))

    return redirect(url_for('index'))

@app.route('/add_state', methods=['POST'])
def add_state():
    if 'username' in session:
        users = mongo.db.users
        states = mongo.db.states
        user_data = users.find_one({'login': session['username']})

        # Создание нового тома
        new_state = {
            '_id': states.count_documents({}),
            'name': request.form.get('name', 'Новая группа'),
            'color': request.form.get('color', '#ffffff')
        }
        
        states.insert_one(new_state)
        user_data['states'].append(new_state['_id'])
        users.update_one({'login': session['username']}, {'$set': {'states': user_data['states']}})
        return redirect(url_for('dashboard'))

    return redirect(url_for('index'))

@app.route('/delete_state/<int:state_id>', methods=['POST'])
def delete_state(state_id):
    if 'username' in session:
        users = mongo.db.users
        user_data = users.find_one({'login': session['username']})
        
        if (state_id in user_data['states']):
            del user_data['states'][user_data['states'].index(state_id)]
        
        users.update_one({'login': session['username']}, {'$set': user_data})
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, url_for, request, render_template, session
from tasks import Task, TaskManager, load_tasks, save_tasks

# ----------   Create app   ---------- #
app = Flask(__name__)
app.secret_key = "asdbfuiasbfiuasbpf"
# ----------   Routes   ---------- #
@app.route('/')  #Home page
def home_page():
    return render_template('home.html')

@app.route('/log', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form.get('username')
        session['user'] = username
        return redirect(url_for('user_page'))
    else:
        if 'user' in session:
            return redirect(url_for('user_page'))
        else:
            return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('log_in'))
    else:
        return render_template('base.html')

@app.route('/user')
def user_page():
    if 'user' in session:
        user = session['user']
        return render_template('userpage.html', username = user)
    else:
        return redirect(url_for('home_page'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('log_in'))

# ----------   Run app   ---------- #
if __name__ == '__main__':
    app.run(debug=True)

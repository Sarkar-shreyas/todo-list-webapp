from flask import Flask, redirect, url_for, request, render_template, session
from tasks import Task, TaskManager, load_tasks, save_tasks

# ----------   Create app   ---------- #
app = Flask(__name__)

# ----------   Routes   ---------- #
@app.route('/')  #Home page
def home_page():
    return render_template('home.html')

@app.route('/<usr>')
def user(usr):
    return render_template('userpage.html', username=usr)



# ----------   Run app   ---------- #
if __name__ == '__main__':
    app.run(debug=True)

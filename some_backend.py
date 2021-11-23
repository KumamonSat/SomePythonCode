import ast
import json
import requests
import ast
from flask import Flask, request, render_template, redirect, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my very secret key,aaaaand i dont give a fuck'


@app.route('/logout', methods=['post', 'get'])
def logout():
    session.clear()
    return redirect('http://localhost:5000/login/')


@app.route('/admin', methods=['post', 'get'])
def admin():
    auth = session.get('authenticated')
    status = session.get('status')

    if authorizeCheck(status, auth) ==  True:
        return render_template('admin.html')
    else:
        return render_template('ban.html')


@app.route('/admin/user/add', methods=['post', 'get'])
def addUser():
    auth = session.get('authenticated')
    status = session.get('status')
    if authorizeCheck(status, auth):
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            group = request.form.get('group')
            status = request.form.get('list')
            password = email
            password = generate_password_hash(password)

            url = 'http://localhost:8081/user/add'
            data = ({"email": email, "username": username, "password": password, "status": status, "group": group})
            resp = ''
            resp = requests.get(url, json=data)
            resp = resp.text
            print(resp)
            return render_template('addUser.html', resp=resp)
        elif request.method == 'GET':
            return render_template('addUser.html')
    else:
        return '404'


def authorizeCheck(status, auth):
    if auth == True:
        if status == 'admin':
            return True
        else:
            return False
    else:
        return False


@app.route('/admin/lesson/add', methods=['POST','GET'])
def addLesson():
    status = session.get('status')
    auth = session.get('authenticated')
    if authorizeCheck(status, auth) == True:
        if request.method == 'GET':
            return render_template('addLesson.html')
        if request.method == 'POST':
            group = request.form.get('group')
            lesson = request.form.get('lesson')
            teacher = request.form.get('teacher')

            url = 'http://localhost:8081/lesson/add'
            data = ({"group": group,"lesson": lesson,"teacher": teacher})
            resp = ''
            resp = requests.get(url, json=data)
            resp = resp.text
            return render_template('addLesson.html', resp=resp)
    else:
        return 'Соси ебало'


@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'GET':
        # auth = session.get('authenticated')
        status = session.get('status')
        group = session.get('group')
        print(group)
        if status == 'user':
            url = 'http://localhost:8082/get/lessons'
            data = ({"group": 'КС-1-17'})
            resp = requests.post(url, json=data)

            resp = resp._content
            resp = resp.decode("utf-8")
            resp = ast.literal_eval(resp)

            return render_template('index.html', resp=resp)


@app.route('/login/', methods=['post', 'get'])
def login():
    if request.method == 'GET':
        message = 'Вы не авторизированы'
        return render_template('login.html', message=message)
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        url = 'http://127.0.0.1:8080/login'
        data = ({"email": username})
        resp = requests.post(url, json=data)

        resp = resp._content
        resp = resp.decode("utf-8")
        resp = ast.literal_eval(resp)

        if check_password_hash(resp[0]['password'], password):
            session['authenticated'] = True
            session['username'] = resp[0]['username']
            session['id'] = resp[0]['id']
            session['group'] = resp[0]['group']
            session['status'] = resp[0]['status']

            return redirect("http://localhost:5000/")
        elif resp[0]['email'] == 'null':
            return redirect("http://localhost:5000/login/")


if __name__ == '__main__':
    app.debug = True
    app.run()


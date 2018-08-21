from flask import Flask, url_for
from flask import request
from flask import json


app = Flask(__name__)

# Method One: curl http://127.0.0.1:5000/hello?name=dongzheng
@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


# Method Two/First: curl http://127.0.0.1:5000/articles/abc
# Output: You are reading abc
# Method Two/Second: curl http://127.0.0.1:5000/articles
# Output: List of /articles
@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


# Method Three:
# C:\Users\zheng>curl -X Get http://127.0.0.1:5000/echo
# ECHO: GET
@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


from werkzeug.utils import secure_filename
import os

# Method Four: see Client\__init__.py

# app.config['UPLOAD_FOLDER'] = 'D:\\PyFlaskLearningProjects\\20180613_Test1\\static\\uploads'
# The route below is used for Ubuntu, upside for Windows
app.config['UPLOAD_FOLDER'] = '/var/www/demoapp/20180614'

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):

        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        return 'hello, '+request.form.get('name', 'little apple')+'. success'
    else:
        return 'hello, '+request.form.get('name', 'little apple')+'. failed'


if __name__ == "__main__":

    # app.run(host='127.0.0.1', port=5001)
    # Below for Ubuntu, upside for Windows
    app.run(host='0.0.0.0', port=5001)
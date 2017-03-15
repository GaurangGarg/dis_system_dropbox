__author__ = 'gaurang'


from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
import requests
# import redis
# r = redis.StrictRedis(host='localhost', port=6379, db=0)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path="/Users/mvp4gman/317/project/") # WSGI app
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # restrict file upload size to 16 MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # validate user input for file name
            data = file.read()
            r = requests.post('http://127.0.0.1:6002/set', data={'key': filename, 'value': data})


            return redirect(request.url)
    return app.send_static_file("index.html")


@app.route('/get', methods=['POST'])
def get():
    filename = request.form.get('filename', '')
    r = requests.post('http://127.0.0.1:6002/get', data={'key': filename})
    return r.text


if __name__ == "__main__":
    app.run(port=6001) # 127.0.0.1:5000 by default

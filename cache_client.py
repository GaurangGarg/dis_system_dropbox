from flask import Flask, request
import PythonCache

app = Flask(__name__) # WSGI app

cache = PythonCache.PythonCache()


@app.route('/get', methods=['POST'])
def get():
    response = ''

    if request.method == 'POST':
        key = request.form.get('key')
        response = cache.get(key)
        response = response.get('value')

    return response


@app.route('/set', methods=['POST'])
def set():
    if request.method == 'POST':
        key = request.form.get('key')
        value = request.form.get('value')
        cache.update(key, value)
    return ''


if __name__ == "__main__": # upgrade flask to latest version > 0.11 so can run app from CLI
    app.run(port=6002) # 127.0.0.1:5000 by default

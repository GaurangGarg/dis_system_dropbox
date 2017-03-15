__author__ = 'gaurang'


from flask import Flask, request, json
import requests

from cassandra import ConsistencyLevel, ReadTimeout
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "files"

app = Flask(__name__) # WSGI app

cluster = Cluster(['52.40.197.16', '52.11.0.58', '54.70.142.196', '54.70.139.205', '52.27.28.162'])
session = cluster.connect()
session.set_keyspace(KEYSPACE)


@app.route('/post', methods=['POST'])
def post():
    response = ''
    if request.method == 'POST':
        filename = request.form.get('key')
        data = request.form.get('data')
        r = requests.post('http://127.0.0.1:6002/set', data={'key': filename, 'value': data})
        query = SimpleStatement("""
                INSERT INTO fileinfo (filename, filecontent)
                VALUES (%(key)s, %(value)s)
                """, consistency_level=ConsistencyLevel.ANY)
        session.execute(query, dict(key=filename, value=data))
    return response


@app.route('/get', methods=['POST'])
def get():
    filename = request.form.get('key', '')
    if not filename:
        return filename

    query = "SELECT * FROM fileinfo WHERE filename=%s"

    future = session.execute_async(query, [filename])

    r = requests.post('http://127.0.0.1:6002/get', data={'key': filename})

    file_content = ''
    data = {}

    try:
        rows = future.result()
        file = rows[0]
        file_content = file.filecontent
        data['db'] = file_content
    except ReadTimeout:
        print "Query timed out"
    except Exception as e:
        print e.message

    if not r or file_content == r.text:
        data['cache'] = r and r.text
        res = requests.post('http://127.0.0.1:6002/delete', data={'key': filename})
        data['consistent'] = 'Consistent'
    else:
        data['cache'] = r and r.text
        data['consistent'] = 'Inconsistent'

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(port=6001) # 127.0.0.1:5000 by default

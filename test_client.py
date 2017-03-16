import requests
import logging
import uuid
import json

# logging.basicConfig(filename='/home/ubuntu/test.log',level=logging.ERROR)
logging.basicConfig(filename='test.log',level=logging.ERROR)

def post(key, value):
    try:
        r = requests.post('http://127.0.0.1:6001/post', data={'key': key, 'data': value})
    except Exception as e:
        pass

def get(key):
    try:
        r = requests.post('http://127.0.0.1:6001/get', data={'key': key})
        res = json.loads(r.text)
        logging.error("Cache val: {} DB val: {} {}".format(res.get('cache'), res.get('db'), res.get('consistent')))
    except Exception as e:
        logging.error(e.message)


def driver():
    key = uuid.uuid4()
    logging.error("Key: {}".format(key))
    i = 0
    num_writes = 1000
    while i < num_writes:
        value = uuid.uuid4()
        post(key, value)
        get(key)
        i += 1


if __name__ == "__main__":
    driver()

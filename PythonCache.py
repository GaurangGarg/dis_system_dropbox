import datetime

class PythonCache:

    def __init__(self):
        self.cache = {}
        self.size = 5


    def timestamp(self):
        now = datetime.datetime.now()

        return now

  
    def contains(self, key):
        return key in self.cache


    def update(self, key, value):

        if not key in self.cache:
            if len(self.cache) < self.size:
                self.cache[key] = {
                    'timestamp': self.timestamp(),
                    'value': value,
                    'date': self.timestamp().strftime("%A, %d %B %Y %H:%M:%S")
                }
            else:
                self.removeold()
                self.cache[key] = {
                    'timestamp': self.timestamp(),
                    'value': value,
                    'date': self.timestamp().strftime("%A, %d %B %Y %H:%M:%S")
                }
        if key in self.cache:
            if len(self.cache) <= self.size:
                self.cache[key] = {
                    'timestamp': self.timestamp(),
                    'value': value,
                    'date': self.timestamp().strftime("%A, %d %B %Y %H:%M:%S")
                }


    def removeold(self):
        old = None
        for key, value in self.cache.items():
            if old is None:
                old = key
            elif self.cache[key]['timestamp'] < self.cache[old]['timestamp']:
                old = key

        self.cache.pop(old)

    
    def display(self):
        for key, value in self.cache.items():
            print('{key}    {value}   {date}'.format(
                key=key, value=value['value'], date=value['date']))


def main():
    cache = PythonCache()
    cache.update('kevin', '0')
    cache.update('noel', '20')
    cache.update('travis', '40')
    cache.update('constant', '50')
    cache.update('ariana', '60')
    cache.display()

    print('------ Add New Item -----')
    cache.update('starboy', '77')
    cache.display()

    print('------ Add New Item -----')
    cache.update('drake', '200')
    cache.display()    

    print('------ Update Item ------')
    cache.update('ariana', '100')
    cache.display()

if __name__ == '__main__':
    main()
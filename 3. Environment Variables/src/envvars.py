from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def print_envvar():
    return "The ENV variable MYVAR is set to: {}".format(os.getenv('MYVAR'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

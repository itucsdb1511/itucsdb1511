import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teamlist')
def teamlist():
    now = datetime.datetime.now()
    return render_template('teamlist.html', current_time=now.ctime())

@app.route('/riderlist')
def riderlist():
    now = datetime.datetime.now()
    return render_template('riderlist.html', current_time=now.ctime())
    
@app.route('/home')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())
    
if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))

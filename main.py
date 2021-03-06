from flask import Flask, render_template
from export import group_data

import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/api/group/<int:group_id>')
def get_group(group_id):
    return group_data(group_id)

if __name__ == '__main__':
    load_dotenv()
    app.debug = 'True'==os.getenv('DEBUG')
    app.run()
from flask import Flask, render_template
from export import group_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/api/group/<int:group_id>')
def get_group(group_id):
    return group_data(group_id)

if __name__ == '__main__':
    app.debug = True
    app.run()
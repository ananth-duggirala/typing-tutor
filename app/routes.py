from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  user = {'username': 'testUser'}
  posts = [
    {
      'author': {'username': 'Alpha'},
      'body': 'I have a new highscore!'
    },
    {
      'author': {'username': 'Beta'},
      'body': 'Me too!'
    }
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)

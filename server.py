from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:@postgres'
db = SQLAlchemy(app)

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(128), unique=True, nullable=False)

@app.route('/')
def index():
  return jsonify({'service': 'users'})

@app.route('/api/v1/users')
def get_users():
  return jsonify({'test': True})

# Called by gunicorn
def create_app():
  db.create_all()
  return app

if __name__ == '__main__':
  app = start_app()
  app.run(port=3000)

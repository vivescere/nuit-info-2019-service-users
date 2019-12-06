from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost/srv_users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pg-user:pg-password@postgres/srv_users'
db = SQLAlchemy(app)

class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), unique=False, nullable=False)

@app.route('/')
def index():
  return jsonify({'service': 'users'})

@app.route('/api/v1/users')
def get_users():
  return jsonify({'test': True})

@app.route('/api/v1/users', methods=['POST'])
def insert_user():
  fields = ['email', 'password']

  for field in fields:
    if field not in request.json:
      return jsonify({'status': 'error', 'message': f'{field} not in json'})

  hashed_pw = generate_password_hash(request.json['password'])

  new_user = User(email=request.json['email'], password=hashed_pw)

  db.session.add(new_user)
  db.session.commit()

  return jsonify({"status": "success", "user": new_user.id})

@app.route('/api/v1/users/validate', methods=['POST'])
def validate_user():
  if 'token' not in request.json:
    return jsonify({'status': 'error', 'message': 'please pass a "token" field'})

  try:
    decoded = jwt.decode(request.json['token'], 'secret-key', algorithms=['HS256'])
  except Exception as e:
    print(e)
    return jsonify({'status': 'error', 'message': 'invalid token'})

  user = User.query.get(decoded['user_id'])

  if user is None:
    return jsonify({'status': 'error', 'message': 'user not found'})

  return jsonify({
    'status': 'success',
    'user': {
      'id': user.id,
      'email': user.email
    }
  })

@app.route('/api/v1/users/login', methods=['POST'])
def login():
  fields = ['email', 'password']

  for field in fields:
    if field not in request.json:
      return jsonify({'status': 'error', 'message': f'{field} not in json'})

  user = User.query.filter(User.email == request.json['email']).first()

  if user is None:
    return jsonify({'status': 'error', 'message': 'email not found'})

  if not check_password_hash(user.password, request.json['password']):
    return jsonify({'status': 'error', 'message': 'wrong password'})

  token = jwt.encode({'user_id': user.id}, 'secret-key', algorithm='HS256').decode()

  return jsonify({
    'status': 'success',
    'token': token
  })

# Called by gunicorn
def create_app():
  #db.create_all()
  return app

if __name__ == '__main__':
  create_app().run(host='0.0.0.0', port=3000)

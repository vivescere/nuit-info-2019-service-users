from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({'service': 'users'})

@app.route('/api/v1/users')
def get_users():
  return jsonify({'test': True})

if __name__ == '__main__':
  app.run(port=3000)

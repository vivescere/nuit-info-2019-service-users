from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({'service': 'users'})

if __name__ == '__main__':
  app.run(port=3000)

from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, Flask!'


@app.route('/user/<nickname>')
def show_user_profile(nickname):
    return f'Hello, user - {nickname}'


if __name__ == '__main__':
    app.run(debug=True)
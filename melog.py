from flask import Flask

app = Flask(__name__)


@app.route('/')
def meLog():
    return 'Log dat shite'


if __name__ == '__main__':
    app.debug = True #remove for production servers
    app.run()

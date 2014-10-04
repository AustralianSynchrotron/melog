from flask import Flask,render_template

app = Flask(__name__)

import melog.config
import melog.views
#if __name__ == '__main__':
#    app.debug = True #remove for production servers
#    app.run()

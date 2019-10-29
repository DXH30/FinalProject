from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from time import sleep

app = Flask(__name__)
nav = Nav(app)
Bootstrap(app)

# Definisikan fungsi
import os


def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []
    
    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # Removed this line because it was redundant the while will catch
        # it, I left it for history
        # if len(lines_found) > lines:
        #    break

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]
# Selesai Definisi


@nav.navigation()
def mynavbar():
    return Navbar(
            'FINPROJ',
            View('Home', 'index'),
            View('Upload', 'uploadFile'),
            View('Setting', 'Setting'),
            View('Log', 'Stream')
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def uploadFile():
    return render_template('upload.html')

@app.route('/setting')
def Setting():
    return render_template('setting.html')

@app.route('/stream')
def Stream():
#    def generate():
    with open('sjd_alert.full') as f:
        data = f.read().replace('\n', '')
#            yield f.read()
#            sleep(1)
    #return app.response_class(generate(), mimetype='text/plain') 
    return render_template('stream.html', data=data)

if __name__ == '__main__':
    app.run()
    nav.init_app(app)

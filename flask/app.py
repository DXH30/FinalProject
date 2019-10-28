from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

app = Flask(__name__)
nav = Nav(app)
Bootstrap(app)

@nav.navigation()
def mynavbar():
    return Navbar(
            'FINPROJ',
            View('Home', 'index'),
            View('Upload', 'uploadFile'),
            View('Setting', 'Setting')
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

if __name__ == '__main__':
    app.run(debug=True)
    nav.init_app(app)

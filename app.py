from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', Title="Home")

@app.route('/management-and-team')
def managementAndTeam():
    return render_template('managementAndTeam.html', Title="Management And Team")

if __name__ == '__main__':
    app.run(debug=True)

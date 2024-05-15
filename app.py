from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', Title="Home")

@app.route('/who-we-are')
def managementAndTeam():
    return render_template('whoWeAre.html', Title="Who We Are")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import os

app = Flask (__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/us')
def us():
    return render_template('us.html')

if __name__ == '__main__':
    app.run(debug=True)
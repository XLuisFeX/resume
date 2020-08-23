from flask import Flask, render_template, request, redirect
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

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    username=False
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        message = "Welcome: " + username
    if username:
        return render_template('sign_up.html', message=message)
    else:
        return render_template('sign_up.html')



if __name__ == '__main__':
    app.run(debug=True)
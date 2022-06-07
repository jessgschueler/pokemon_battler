from flask import Flask, render_template
@app.route('/user/<name>')
def user(name):
    return render_template('hello.html', name=name)

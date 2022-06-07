@app.route('/user/<name>')
def user(name):
    personal = f'<h1>Hello, {name}!</h1>'
    instruc = '<p>Change the name in the <em>browser address bar</em> \
        and reload the page.</p>'
    return personal + instruc

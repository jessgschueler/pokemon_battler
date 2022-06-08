@app.route("/login")
@login_required
def login():
    logIN_user()
    

forms.py

if form.validate_on_submit():
    try:
        user = User.query.filter_by(email=form.email.data).first()
        if check_password(user.pwd, form.pwd.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid Username or password!", "danger")
    except Exception as e:
        flash(e, "danger")

    return redirect(url_for('login'))


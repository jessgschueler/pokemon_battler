@app.route("/login")
@login_required
def login():
    logIN_user()
    return redirect(url_for('login'))

   if form.validate_on_submit():
       try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")


# if form.validate_on_submit():
#        try:
#             email = form.email.data
#             pwd = form.pwd.data
#             username = form.username.data

#             newuser = User(
#                 username=username,
#                 email=email,
#                 pwd=bcrypt.generate_password_hash(pwd),
#             )

#             db.session.add(newuser)
#             db.session.commit()
#             flash(f"Account Succesfully created", "success")
#             return redirect(url_for("login"))

#         except Exception as e:
#             flash(e, "danger")

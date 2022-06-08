@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

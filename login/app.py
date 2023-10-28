from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secret key for session management

# Simulated user data (replace with a real user database)
users = {
    "admin": "password123",
}

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# @app.route('/patient-login')
# def patient_login():
#     return render_template('patient_login.html')

@app.route('/therapist-login')
def therapist_login():
    return render_template('therapist_login.html')

@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for('dashboard',name = username))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('patient_login.html', error=error)

    return render_template('patient_login.html')

@app.route('/patient/dashboard/<name>')
def dashboard(name):
    if "user" in session:
        username = session["user"]
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('patient_login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('patient_login'))

if __name__ == '__main__':
    app.run(debug=True)

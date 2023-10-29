from flask import Flask, render_template, request, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secret key for session management

# Simulated user data (replace with a real user database)
users = {
    "admin": "password123",
    "patient1": "patient1"
}

patient_details = {
    "admin":1,
    "patient1":0
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
        if database.patient_login_check(username,password):
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
        if username in patient_details and patient_details[username] == 1:
            return render_template('dashboard_with_video_upload.html', username=username)
        else:
            return render_template('dashboard_with_form.html', username=username)
    else:
        return redirect(url_for('patient_login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.clear()
    return redirect(url_for('patient_login'))

@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    if "user" in session:
        if request.method == 'POST':
            question1 = request.form.get("question1")
            question2 = request.form.get("question2")
            question3 = request.form.get("question3")
            question4 = request.form.get("question4")
            # You can now process and store the answers as needed
            return render_template('submission_success.html')
    else:
        return redirect(url_for('patient_login'))
    
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if "user" in session:
        if request.method == 'POST':
            # Handle the video upload here
            uploaded_video = request.files['video']
            if uploaded_video:
                pass
    else:
        return redirect(url_for('patient_login'))




if __name__ == '__main__':
    app.run(debug=True)

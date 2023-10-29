from flask import Flask, render_template, request, redirect, url_for, session
import database
import helper

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

@app.route('/therapist-login', methods=['GET', 'POST'])
def therapist_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if database.therapist_login_check(username, password):
            session["user"] = username
            return redirect(url_for('enter_filename'))  # Redirect to the enter-filename route
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('therapist_login.html', error=error)
    
    # Handle the GET request by rendering the therapist login page
    return render_template('therapist_login.html')


@app.route('/enter-filename', methods=['GET', 'POST'])
def enter_filename():
    success_message = None

    if request.method == 'GET':
        return render_template('filename_input.html')
    
    if request.method == 'POST':
        # Access the 'filename' field from the form
        file_name = request.form.get('filename')

        # Now, you can use the 'file_name' variable as needed
        print(f"File name entered: {file_name}")

        # You can also store the 'file_name' in the session if needed
        if file_name:
            session['file_name'] = file_name  # Store the file name in the session

            # Assume the file processing was successful
            success_message = f"File '{file_name}' was successfully processed."

    # Retrieve the file name from the session (if it was stored)
    processed_file_name = session.get('file_name')
    link = helper.create_signed_url(processed_file_name)
    output = helper.lookup(link)
    print(output)
    return render_template('filename_input.html', success_message=success_message, processed_file_name=output)



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
        if database.session_check_data(username):
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

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    print("in app route")
    if "user" in session:
        if request.method == 'POST':
            question1 = request.form.get("question1")
            question2 = request.form.get("question2")
            question3 = request.form.get("question3")
            question4 = request.form.get("question4")

            database.patient_insert_data(session["user"],question1,question2,question3,question4)
            # You can now process and store the answers as needed
            response_data = {"message": "Data received and processed successfully"}
       
            return render_template('submission_success.html')
    else:
        return redirect(url_for('patient_login'))


@app.route('/upload-video-link', methods=['POST'])
def upload_video_link():
    if "user" in session:
        if request.method == 'POST':
            video_link = request.form.get("video-link")
            
            # Now you can process and store the video link as needed
            
            return render_template('submission_success.html')
    else:
        return redirect(url_for('patient_login'))



if __name__ == '__main__':
    app.run(debug=True)

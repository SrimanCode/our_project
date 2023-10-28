from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

@app.route('/patient-login')
def patient_login():
    return render_template('patient_login.html')

@app.route('/therapist-login')
def therapist_login():
    return render_template('therapist_login.html')

if __name__ == '__main__':
    app.run(debug=True)

# ... [Previous code]
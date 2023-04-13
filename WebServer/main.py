from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

appFlask = Flask(__name__)
appFlask.secret_key = "27eduCBA09"

@appFlask.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        studentName = request.form['studentName']
        website = request.form.get('website')
        return 'Submitted!'
    return '''<form method = "post">
    <p>Enter Name:</p>
    <p><input type = "text" name = "studentName" /></p>
    <p>Enter Website:</p>
    <p><input type = "text" name = "website" /></p>
    <p><input type = "submit" value = "submit" /></p>
    </form>'''

if __name__ == "__main__":
    try:
        appFlask.run(port=5002, debug=True)
    except KeyboardInterrupt:
        exit()
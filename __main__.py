#!/usr/bin/env python
import os
from flask import Flask, render_template, Response,redirect,url_for,request,flash
from camera_opencv import Camera


app = Flask(__name__)
app.secret_key  = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'



@app.route('/')
@app.route('/logout')
def index():
    """Video streaming home page."""
    return render_template('login.html')



def camera():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    try:
        if request.method == "POST":
            print(1123)
            attempted_username = request.form['username']
            attempted_password = request.form['pass']
           
            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                # return redirect(url_for('camera'))
                return render_template('index.html')  
            else:
                error = "Invalid credentials. Try Again."   
                return render_template("index.html", error = error)
        if request.method == "GET":
            return render_template("index.html")
            
    except Exception as e:
        flash(e)
        return render_template("index.html", error = e)  

def gen(camera,command=None):
    """Video streaming generator function."""
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if command:
                break
    except Exception as e:
        print(e)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

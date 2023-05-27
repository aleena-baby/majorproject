from flask import Flask, request, render_template
import os

app = Flask(__name__)
is_alert_active = True

@app.route('/index')
def home():
    return render_template('index.html', alert_status=is_alert_active)

@app.route('/recognize', methods=['GET'])
def recognize():
    if is_alert_active:
        os.system("python 03_face_recognition.py")
    return "Face recognition script executed successfully."

@app.route('/alert', methods=['GET', 'POST'])
def set_alert_status():
    global is_alert_active
    if request.method == 'POST':
        status = request.form['status']
        is_alert_active = bool(int(status))
    return str(int(is_alert_active))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

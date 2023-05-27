from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/recognize', methods=['GET'])
def recognize():
    os.system("python 03_face_recognition.py")
    return "Face recognition script executed successfully."

@app.route('/update/delete', methods=['GET'])
def update_delete():
    os.system("python 01_face_datasetdelete.py")
    return "Face dataset delete script executed successfully."

@app.route('/update/add', methods=['GET'])
def update_add():
    os.system("python 01_face_datasetadd.py")
    return "Face dataset add script executed successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

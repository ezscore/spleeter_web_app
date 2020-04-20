import os
#from functions import *
from flask import Flask, render_template, request, send_file
from spleeter.separator import Separator
from werkzeug.utils import secure_filename


def separate_file(initial, destination):
    separator = Separator('spleeter:2stems')
    print(initial, destination)
    print('this is where it fails')
    separator.separate_to_file(initial, destination)

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    target = os.path.join(APP_ROOT, 'spleet_files')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    #for file in request.files.getlist("file"):
    file = request.files['file']
    filename = secure_filename(file.filename)

    destination = os.path.join(APP_ROOT, filename)
    print(APP_ROOT)
    print(filename)
    print(os.path.join(APP_ROOT, filename))
    # file.save(filename)

    file.save(os.path.join(target, filename)) #saves file to folder

    separate_file(os.path.join(target, filename), filename)
    # os.path.join(APP_ROOT, filename) = /Users/grayangelo/spleeter_app/06_-_Avicii_-_Broken_Arrows.mp3 -> next directory -> return all files
    #walk through splitted files

    roots = []
    dir1 = []
    file1 = []
    for root, dirs, files in os.walk(destination, topdown=True): #crawl through directory saving each root, dir, and file
        roots.append(root)
        dir1.append(dirs)
        file1.append(files)

    path_to_file = roots[1] + "/" + file1[1][1] #the path for the relevant files (vocals)

    return send_file(
        path_to_file,
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="vocal.wav")

if __name__ == "__main__":
    app.run(port=4555, debug=True)

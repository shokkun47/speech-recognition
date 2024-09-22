from flask import Flask, render_template, jsonify, request
import subprocess
import os
import datetime

app = Flask(__name__)
p = ""
def get_text(fn):
    texts = ""
    if os.path.exists(f"history/{fn}"):
        with open(f"history/{fn}", 'r') as fp:
            texts = "".join([i for i in fp])
    else:
        texts = 'starting the whisper speech recognition process...'
    return texts

def start_process(unix_time):
    global p
    cmd = f"python whisper_mic/mic.py --time {unix_time}"
    p = subprocess.Popen(cmd.split())
    return p

@app.route('/')
def index():
    name = "Keiji"
    return render_template("index.html", name=name)

@app.route('/get_item', methods=['POST'])
def get_item():
    fn = request.json['rfn']
    print(fn)
    item = get_text(fn)
    return jsonify({'item':item})

@app.route('/start_recog', methods=['POST'])
def start_recog():
    if not os.path.exists("history"):
        os.mkdir("history")
    unix_time =  round(datetime.datetime.now().timestamp())
    fn = f"recognized{unix_time}"
    p = start_process(unix_time)
    return jsonify({'item':fn})

@app.route('/stop', methods=['POST'])
def stop():
    global p
    item = ""
    try:
        if p:
            p.kill()
        item = "success"
    except:
        item = "failed to stop the process"

    return jsonify({'item':item})    

if __name__ == '__main__':


    app.run(debug=True)
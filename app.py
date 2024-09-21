from flask import Flask, render_template, jsonify
import random
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_item", methods=["POST"])
def get_item():
    items = ["apple", "peach", "orange", "pineapples"]
    item = random.choice(items)
    return jsonify({"item":item})

if __name__ == "__main__":
    cmd = f"python whisper_mic/mic.py"
    subprocess.Popen(cmd.split())
    app.run(debug=True)

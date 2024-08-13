from ramapi import *
import random
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    charID = random.randint(1,826)
    char = ramapi.Character.get(charID)
    name = char['name']
    print(name)

    return render_template('index.html', char=char, name=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


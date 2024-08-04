from ramapi import *
import random
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    charID = random.randint(1,826)
    char = ramapi.Character.get(charID)
    return f'''
<h1>{char['name']}</h1>

<img src="{char['image']}">
'''




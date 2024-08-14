from ramapi import *
import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def main():
    charID = random.randint(1,826)

    while charID in [19,66,104,189,249]:
        charID = random.randint(1,826)

    char = ramapi.Character.get(charID)
    global name
    name = char['name']

    results = ramapi.Character.filter(name=name)

    amntofEpisodes = 0
    seenIn = []
    origin = ''
    latestLocation = ''
    for result in results['results']:

        if len(result['episode']) > amntofEpisodes:
            amntofEpisodes = len(result['episode'])
            origin = result['origin']['name']
            latestLocation = result['location']['name']

        for episode in result['episode']:
            season = 0
            episodeNum = episode[-2:]
            if episodeNum[0] == '/':
                episodeNum = episodeNum[1]
            episodeNum = int(episodeNum)

            if episodeNum <= 11:
                season = 1
                seenIn.append(f'Season {season} Episode {episodeNum}')
            else:
                episodeNum -= 11
                season = 1
                while episodeNum > 0:
                    season += 1
                    episodeNum -= 10
                    if episodeNum <= 0:
                        seenIn.append(f'Season {season} Episode {10+episodeNum}')
            


    seenIn = list(dict.fromkeys(seenIn))
    seenIn.sort()

    return render_template('index.html', char=char, name=name, seenIn=seenIn, latestLocation=latestLocation, origin=origin)

@app.route("/help")
def help():
    return render_template('help.html')

@app.route('/check_guess', methods=['POST'])
def check_guess():
    user_guess = request.json.get('guess')
    character_name = name

    if user_guess == character_name:  
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


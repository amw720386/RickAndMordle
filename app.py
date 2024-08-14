from ramapi import *
import random
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    charID = random.randint(1,826)

    while charID in [19,66,104,189,249]:
        charID = random.randint(1,826)

    charID = 1

    char = ramapi.Character.get(charID)
    name = char['name']

    results = ramapi.Character.filter(name=name)

    originUnknown = False
    lastSeenUnknown = False
    seenIn = []
    origin = ''
    latestLocation = ''
    for result in results['results']:

        if not result['origin']['url']:
            originUnknown = True

        if not originUnknown:
            if result['origin']['url'][-2] == '/':
                if origin == '':
                    origin = int(result['origin']['url'][-1])   
                elif int(result['origin']['url'][-1]) < origin:
                    origin = int(result['origin']['url'][-1])
            else:
                if origin == '':
                    origin = int(result['origin']['url'][-2:])   
                elif int(result['origin']['url'][-2:]) < origin:
                    origin = int(result['origin']['url'][-2:])

        if not result['location']['url']:
            lastSeenUnknown = True

        if not lastSeenUnknown:                
            if result['location']['url'][-2] == '/':
                if latestLocation == '':
                    latestLocation = int(result['location']['url'][-1])             
                elif int(result['location']['url'][-1]) > latestLocation:
                    latestLocation = int(result['location']['url'][-1])
            else:
                if latestLocation == '':
                    latestLocation = int(result['location']['url'][-2:])   
                elif int(result['location']['url'][-2:]) > latestLocation:
                    latestLocation = int(result['location']['url'][-2:])

        originUnknown = False
        lastSeenUnknown = False

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

    print(seenIn)

    if origin == '':
        origin = 'Unknown'
    else:
        origin=ramapi.Location.get(origin)['name']
    if latestLocation == '':
        latestLocation = 'Unknown'
    else:
        latestLocation=ramapi.Location.get(latestLocation)['name']

    return render_template('index.html', char=char, name=name, seenIn=seenIn, latestLocation=latestLocation, origin=origin)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


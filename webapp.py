import flask
from flask import render_template, request, redirect, url_for
import sys
import os
from backend.datasource import *
from backend.wordCloudGenerator import *
import numpy as np
import matplotlib.pyplot as plt


app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

d = DataSource()

def representsInt(y):
    try:
        int(y)
        return True
    except ValueError:
        return False

def representsRange(r):
    try:
        dashSplit = r.split('-')
        commaSplit = r.split(',')
        if len(dashSplit) == 2 and representsInt(dashSplit[0]) and representsInt(dashSplit[1]):
            return dashSplit
        elif len(commaSplit) == 2 and representsInt(commaSplit[0]) and representsInt(commaSplit[1]):
            return commaSplit
        else:
            return []
    except SyntaxError:
        return []
def representsWord(w):
    if w.startswith("\'") and w.endswith("\'") and len(w)>1:
        return representsWord(w[1:-1])
    elif w.startswith("\"") and w.endswith("\"") and len(w)>1:
        return representsWord(w[1:-1])
    elif isinstance(w, str):
        return w
    else:
        return False

@app.route('/')
@app.route('/query/')
@app.route('/query')
def home():
    return render_template('home.html')


def sendToHome():
    return redirect(url_for('home.html'))

@app.route('/info.html')
def infoPage():
    return render_template('info.html')

@app.route('/error')
def showError():
    return render_template('error.html')

@app.route('/query/<query>')
def helperFunction(query):
    # Redirects query (which may be a year or word or range)
    # to necessary page.
    query = str(query)
    query = query.lower()
    if representsInt(query):
       return showYearData(int(query))
    elif representsRange(query):
        yearRange = representsRange(query)
        return showYearRangeData(yearRange)
    elif representsWord(query):
        word = representsWord(query)
        return showWordData(word)
    else:
        errorMsg = "Something went wrong"
        return render_template('error.html', errorMsg=errorMsg)

@app.route('/year/<year>/')
def showYearData(year):
    d = DataSource()
    topSongs = d.getTopXSongsInYear(year, 100)
    topWords = d.getTopXWordsInYear(year, 200)

    if topSongs != None and topWords != None:
        wordCloud = wordCloudGenerator(topWords)
        wordCloud.generateWordCloudPNG()
        os.replace("wordCloud.png", "static/wordCloud.png")
        return render_template('year.html', year=year, topWords=topWords, topSongs = topSongs)
    else:
        errorMsg = "Invalid year entry. This data only looks at years 1965-2015"
        return render_template('error.html', errorMsg=errorMsg)


@app.route('/word/<word>/')
def showWordData(word):
    d = DataSource()
    topSongs = d.getTopXSongsWithMyWord(word,25)

    if topSongs != None and len(topSongs) != 0:
        graphYears = list(range(1965, 2016))
        graphCounts = d.getWordTrendList(word)
        plt.clf()
        plt.plot(graphYears, graphCounts)
        plt.xlabel('Years (1965-2015)')
        plt.ylabel('Frequency')
        plt.title('Usage by Years for ' + word)
        plt.xticks(np.arange(1965, 2016, step=5))

        plt.savefig('static/new_plot.png')
        return render_template('word.html', word=word, topSongs=topSongs)
    else:
        errorMsg = "Invalid word entry, the word was either not found in  the database , or entered incorrectly"
        return render_template('error.html', errorMsg=errorMsg)



@app.route('/yearrange/<year1>/<year2>/')
def showYearRangeData(yearRange):
    startYear = int(yearRange[0])
    endYear = int(yearRange[1])
    d = DataSource()
    topWords = d.getTopXWordsInYearRange(startYear, endYear, 200)
    if topWords != None:
        wordCloud = wordCloudGenerator(topWords)
        wordCloud.generateWordCloudPNG()
        os.replace("wordCloud.png", "static/wordCloud.png")
        return render_template('yearrange.html', startYear=startYear, endYear=endYear, topWords=topWords)
    else:
        errorMsg = "Invalid year range entry. This data only looks at years 1965-2015 and you must write the earlier year first (ex. 1975-1984)."
        return render_template('error.html', errorMsg=errorMsg)


@app.route('/artist/<artist>/')
def showArtistData(artist):
    artist = artist.split('%20')
    artist = " ".join(artist)
    artist = artist.lower()

    d = DataSource()
    topWords = d.getTopXWordsofArtist(artist,50)
    if topWords != None and topWords != 0:
        wordCloud = wordCloudGenerator(topWords)
        wordCloud.generateWordCloudPNG()
        os.replace("wordCloud.png", "static/wordCloud.png")
        return render_template('artist.html', artist=artist, topWords=topWords)
    else:
        errorMsg = "We cannot find that artist"
        return render_template('error.html', errorMsg=errorMsg)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

import pafy
import ffmpeg
import os
import uuid 
import shutil
import asyncio
from convert import *
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_socketio import SocketIO,emit, send
from mp3_tagger import MP3File
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x1a\x95\xe3A\xd9\x03Z-\xe8\xbb\xb4\x7f\x1f\xb63p'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

socketio = SocketIO(app)


urls = ""
dir = ""
album = ""

@socketio.on("connect")
def connectMsg():
    print("user connected")


# Download Audio
async def changeAudio(x,dir,artist,album):
    playlist = ""
    try:
        playlist = pafy.get_playlist(x)
        for x in range(len(playlist) - 1 ):
            playlist['items'][x]['pafy'].getbestaudio(preftype="m4a").download(filepath=dir)
            socketio.emit('Working')
            print(x)
    except OSError as e:
        print(e)
        return 'no video formats found...try again'
    except IndexError as e:
        print(e)
    except Exception as e:
        print(e)
        return e
  
@app.route("/")
def hello():
    try:
        return render_template("index.html")
    except Exception:
        return "Uh Oh Something Broke!! We'll get our Monkey's On It"


@app.route("/audio", methods=['GET','POST'])
def getAudio():
    #get form data
    url = request.form['val']
    artist = request.form['albumArtist']
    album = request.form['albumName']
    
    #create tmp dir
    my_id = uuid.uuid1()
    dir = "Dir-" + str(my_id)
    os.mkdir(dir)

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(changeAudio(url,dir,artist,album))
    #asyncio.run(changeAudio(url,dir,artist,album))
    
    return redirect(url_for('mp3' , artist=artist, album=album, dir=dir))


@app.route("/mp3/<artist>/<album>/<dir>")
def mp3(artist,album,dir):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(toMp3(artist,album,dir))
    #asyncio.run(toMp3(artist,album,dir))
    return redirect(url_for('zipAlbum', album=album, dir=dir))


@app.route("/zip/<album>/<dir>")
def zipAlbum(album,dir):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(toAlbum(album,dir))
    #asyncio.run(toAlbum(album,dir))
    return redirect(url_for('sendZip', album=album))

@app.route("/sendfile/<album>")
def sendZip(album):
    zipFile = album + ".zip"
    return send_file(zipFile)



    
if __name__ == "__main__":
    socketio.run(app)


'''
def clearDirs():
    os.chdir("tmp")
    tmpList = os.listdir("tmp")
    for x in tmpList:
        try:
            shutil.rmtree("app/tmp/" + x)
        except Exception:
            print(x + " was not deleted")
    print(os.listdir("tmp"))
    

sched = BackgroundScheduler(daemon=True)
sched.add_job(clearDirs,'interval',minutes=2)
sched.start()
'''
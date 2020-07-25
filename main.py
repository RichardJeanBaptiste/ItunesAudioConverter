import pafy
import ffmpeg
import os
import uuid 
import shutil
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO,emit, send
from mp3_tagger import MP3File
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x1a\x95\xe3A\xd9\x03Z-\xe8\xbb\xb4\x7f\x1f\xb63p'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

cwd = os.getcwd()
print("this is ----" + cwd)

def clearDirs():
    os.chdir("tmp")
    tmpList = os.listdir("tmp")
    for x in tmpList:
        try:
            shutil.rmtree("tmp/" + x)
        except Exception:
            print(x + " was not deleted")
    

sched = BackgroundScheduler(daemon=True)
sched.add_job(clearDirs,'interval',minutes=5)
sched.start()

def changeAudio_message():
    socketio.emit('changeAudio', 'Getting Url')

def toMp3_message():
    socketio.emit('toMp3', 'To Mp3')

def toAlbum_message():
    socketio.emit('toAlbum', 'To Album')

def startOver():
    socketio.emit('startOver', 'start again')


def changeAudio(x,dir):
    changeAudio_message()
    playlist = pafy.get_playlist(x)
    for x in range(len(playlist) - 1):
        try:
            playlist['items'][x]['pafy'].getbestaudio().download(filepath=dir)
        except OSError:
            return 'no video formats found...try again'
        except IndexError:
            pass

def toMp3(artist,album,dir):
    #toMp3_message()
    urls = os.listdir(dir)
    for x in urls:
        try:
            name = dir + "/" + x[:-5] + '.mp3'
            print(name)
            songUrl = dir + "/" + x
            stream = ffmpeg.input(songUrl)
            stream = ffmpeg.output(stream, name)
            ffmpeg.run(stream)
            mp3 = MP3File(name)
            mp3.artist = artist
            mp3.album = album
            mp3.save()
            os.remove(songUrl)
        except Exception as e:
            print(e)


def toAlbum(album,dir):
    try:
        #toAlbum_message()
        albumDir = "zip/" + album
        shutil.make_archive(albumDir, 'zip', dir)
    except Exception as e:
        print(e)
    
    
    
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
    dir = "tmp/testDir-" + str(my_id)
    os.mkdir(dir)
    changeAudio(url,dir)
    toMp3(artist,album,dir)
    toAlbum(album,dir)
    zipFile = "zip/" + album + ".zip"
    #startOver()
    return send_file(zipFile)

if __name__ == "__main__":
    #socketio.run(app)
    app.run()
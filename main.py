from flask import Flask, render_template, request, send_file, redirect, url_for,request, Response
from convert import getAudioFromPafy, toMp3, zipDirectory
from playlistClass import Playlist 
import uuid
import os

app = Flask(__name__)

''''
app.config['SECRET_KEY'] = b'\x1a\x95\xe3A\xd9\x03Z-\xe8\xbb\xb4\x7f\x1f\xb63p'
'''
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

workingPlaylist = Playlist("","","")

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/audio", methods=['POST'])
def route():
    try:
        #get form data
        url = request.form['val']
        artist = request.form['albumArtist']
        album = request.form['albumName']

        #create tmp dir
        my_id = uuid.uuid1()
        dir = "Dir-" + str(my_id)
        os.mkdir(dir)

        workingPlaylist = Playlist(artist,album,dir)

        workingPlaylist.artistName = artist
        workingPlaylist.artistAlbum = album
        workingPlaylist.currDir = dir

        return getAudioFromPafy(url,workingPlaylist)
    except Exception as e:
        return e
    

@app.route("/toMp3/<artist>/<album>/<dir>")
def toMp3Route(artist,album,dir):
    return toMp3(artist, album, dir)

@app.route("/toZip/<album>/<dir>")
def toZipRoute(album,dir):
    zipDirectory(album,dir)
    zipFile = album + ".zip"
    dir = album + ".zip"
    return send_file(dir)

    
if __name__ == "__main__":
    app.run()
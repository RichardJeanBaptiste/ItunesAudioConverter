import pafy
from mp3_tagger import MP3File
from flask import Flask, render_template, request, send_file, redirect, url_for,make_response
import ffmpeg
import os
import shutil

# Download Audio
def getAudioFromPafy(url,workingPlaylist):
    
    dir = workingPlaylist.currDir
    playlist1 = ""
    try:
        playlist1 = pafy.get_playlist(url)
        listLength = len(playlist1['items'])
        for x in range(listLength):
            reponse = make_response("abds")
            playlist1['items'][x]['pafy'].getbestaudio(preftype="m4a").download(filepath=dir)
        
        workingPlaylist.setZipDir(dir)
        return redirect(url_for('toMp3Route',artist=workingPlaylist.artistName,album=workingPlaylist.artistAlbum, dir=workingPlaylist.currDir))
    except OSError as e:
        print(e)
        return 'no video formats found...try again'
    except IOError as e:
        return 'IOerror'
    except Exception as e:
        print(e)
        return e


        
# convert files to mp3 format
def toMp3(artist,album,dir):
    try:
        urls = os.listdir(dir)
        for x in urls:
            name = dir + "/" + x[:-5] + '.mp3'
            songUrl = dir + "/" + x
            stream = ffmpeg.input(songUrl)
            stream = ffmpeg.output(stream, name)
            ffmpeg.run(stream)
            mp3 = MP3File(name)
            mp3.artist = artist
            mp3.album = album
            mp3.save()
            os.remove(songUrl)
         
        return redirect(url_for('toZipRoute',album=album,dir=dir))
    except Exception as e:
        print(e)


# Create zip directory 
def zipDirectory(album,dir):
    try:
        albumDir = "zip/" + album
        albumDir = album
        shutil.make_archive(albumDir, 'zip', dir)
    except Exception as e:
        print(e)




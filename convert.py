import pafy 
import ffmpeg
import os
import asyncio
import shutil
from mp3_tagger import MP3File


# Download Audio
async def changeAudio(x,dir,artist,album):
    playlist = ""
    try:
        playlist = pafy.get_playlist(x)
        for x in range(len(playlist) - 1 ):
            playlist['items'][x]['pafy'].getbestaudio(preftype="m4a").download(filepath=dir)
            print(x)
    except OSError as e:
        print(e)
        return 'no video formats found...try again'
    except IndexError as e:
        print(e)
    except Exception as e:
        print(e)
        return e
    

#asyncio.run(changeAudio("https://www.youtube.com/watch?v=xdGLK_sOWb0","a","a","a"))

# convert files to mp3 format
async def toMp3(artist,album,dir):
    #toMp3_message()
    try:
        urls = os.listdir(dir)
        for x in urls:
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


# Create zip directory 
async def toAlbum(album,dir):
    try:
        albumDir = "zip/" + album
        albumDir = album
        shutil.make_archive(albumDir, 'zip', dir)
    except Exception as e:
        print(e)


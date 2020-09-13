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



'''


#socketio = SocketIO(app)


urls = ""
dir = ""
album = ""


# Download Audio
async def changeAudio(x,dir,artist,album):
    playlist = ""
    try:
        playlist = pafy.get_playlist(x)
        for x in range(len(playlist) - 1 ):
            await playlist['items'][x]['pafy'].getbestaudio(preftype="m4a").download(filepath=dir)
    except OSError as e:
        print(e)
        return 'no video formats found...try again'
    except IndexError as e:
        print(e)
    except Exception as e:
        print(e)

def createMp3(name, artist):
    mp3 = MP3File(name)
    mp3.artist = artist
    mp3.album = album
    mp3.save()

# convert files to mp3 format
async def toMp3(artist,album,dir):
    #socketio.emit('Converting')
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
            #createMp3(name,artist)
            os.remove(songUrl)
    except Exception as e:
        return e

# Create zip directory 
async def toAlbum(album,dir):
    try:
        #socketio.emit('ZipFile')
        albumDir = "zip/" + album
        albumDir = album
        shutil.make_archive(albumDir, 'zip', dir)
    except Exception as e:
        print(e)

@app.route("/")
def hello():
    try:
        return render_template("index.html")
    except Exception:
        return "Uh Oh Something Broke!! We'll get our Monkey's On It"

@app.route("/audio")
def getAudio():
    #changeAudio(url,dir,artist,album)
    return "asd"


@app.route("/test")
def test():
    return "Hello from tests"









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
    
    return redirect(url_for('mp3' , artist=artist, album=album, dir=dir))


@app.route("/mp3/<artist>/<album>/<dir>")
def mp3(artist,album,dir):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(toMp3(artist,album,dir))
    return redirect(url_for('zipAlbum', album=album, dir=dir))


@app.route("/zip/<album>/<dir>")
def zipAlbum(album,dir):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(toAlbum(album,dir))
    return redirect(url_for('sendZip', album=album))

@app.route("/sendfile/<album>")
def sendZip(album):
    zipFile = album + ".zip"
    #socketio.emit('startOver')
    return send_file(zipFile)

'''
  

'''

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
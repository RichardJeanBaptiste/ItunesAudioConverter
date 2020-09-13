class Playlist:
    def __init__(self,artistName,artistAlbum,currDir):
        self.artistName = artistName
        self.artistAlbum = artistAlbum
        self.currDir = currDir
        self.zipDir = ""
    
    def setZipDir(self,dir):
        zipDir = dir
    
        
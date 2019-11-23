from colorama import Fore, Back, Style, init
import vlc
import time
from pytube import YouTube, Playlist
from pathlib import Path
import os
import html
import hjson

def print_color(text, argcolor = "white"):
    '''
    Prints using colorama
    '''

    if argcolor == "white":
        color = Fore.WHITE
    elif argcolor == "green":
        color = Fore.GREEN
    elif argcolor == "magenta":
        color = Fore.MAGENTA
    elif argcolor == "grey":
        color = Fore.LIGHTBLACK_EX
    elif argcolor == "pink":
        color = Fore.LIGHTRED_EX        
    guardColor = Fore.LIGHTBLACK_EX
    print(color, text, guardColor)


class SlothPlayer():

    def __init__(self, config_file="config.txt"):
        #self.instance = vlc.Instance("--novideo",  "--quiet")
        self.configuration_file = config_file
        self.instance = vlc.Instance("--novideo",  "--quiet")
        self.player = self.instance.media_player_new()
        self.npressed = False
        self.ppressed = False
        self.songs_played = 0
        self.init_time = time.time()
        self.refreshFrequency = 10 #Hz


    
    def getPlaylistLinks(self, url):

        playlist = Playlist(url)
        playlist.populate_video_urls()

        output = playlist.video_urls

        return output

    def printconfig(self):

        print_color(f"Local Folders: {self.localMusicFolders}")
        print_color(f"Active: {self.localMusicFoldersActive}")
        print_color(f"Youtube Playlists: {self.youtubePlaylists}")
        print_color(f"Active: {self.youtubePlaylistsActive}")
        print_color(f"Silence Interval: {self.interval}")
        print_color(f"{len(self.songfiles)} music files found.")



    def loadconfig(self):

        try:
            with open(self.configuration_file, encoding='utf-8') as config_file:
                data = hjson.load(config_file)
                
        except IOError:
            raise IOError("Couldn't open configuration file")

        self.localMusicFolders = data['localMusicFolders']
        self.localMusicFoldersActive = data['localMusicFoldersActive']
        self.youtubePlaylists = data['youtubePlaylists']
        self.youtubePlaylistsActive = data['youtubePlaylistsActive']
        self.consecutiveReadings = data['consecutiveReadings']
        self.maxSongPlayTime = data['maxSongPlayTime']
        self.fileTypes = data['fileTypes']
        self.interval = data['interval']
        self.songfiles = self.__fetchsongs()
        
        return True

    def __fetchsongs(self):
        
        soundfiles = []

        if self.localMusicFoldersActive:
            for localMusicFolder in self.localMusicFolders:
                for fileType in self.fileTypes:
                    for filename in Path(localMusicFolder).rglob(fileType):
                        soundfiles.append(str(filename))


        if self.youtubePlaylistsActive:
            for youtubePlaylist in self.youtubePlaylists:
                youtubePlaylistLinks = self.getPlaylistLinks(youtubePlaylist)

                soundfiles = soundfiles + youtubePlaylistLinks

        return soundfiles
        

    def play(self, song):
        #movie is the YouTube or a local URL

        self.instance = vlc.Instance("--novideo",  "--quiet")
        self.player = self.instance.media_player_new()

        instance = self.instance
        player = self.player


        media = instance.media_new(song)
        media_list = instance.media_list_new([song]) #A list of one song
        
        player.set_media(media)
        self.player.audio_set_volume(100)

        if 'youtube.com' in song:
            song_title = html.unescape(YouTube(song).title)
        else:
            song_title = ""

        #Create a new MediaListPlayer instance and associate the player and playlist with it
        list_player =  instance.media_list_player_new()
        list_player.set_media_player(player)
        list_player.set_media_list(media_list)

        player.play()
        return song_title

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def resume(self):
        self.player.play()

    def get_state(self):
        return self.player.get_state()


if __name__ == "__main__":

    import time
    
    slothplayer = SlothPlayer("config.txt")
    shortsong = u'https://www.youtube.com/watch?v=EzKImzjwGyM'
    longsong = u"https://www.youtube.com/watch?v=sksNCp00R7U"
    
    song = longsong

    slothplayer.play(song)

    playing = set([0,1,2,3,4])

    time.sleep(5)

    slothplayer.pause()

    time.sleep(5)

    slothplayer.resume()

    time.sleep(10)

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

    """
    Model of the player. Fetch configuration and instantiate a vlc player through vlc-python binding.
    
    """

    def __init__(self, config_file="config.txt"):
        """
        Initializer of the class.

        Args:
            config_file (str): configuration file, by default "config.txt"
        
        """
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
        """Gets youtube playlist from a url.

        Args:
            url (str): The youtube url.

        Returns:
            output (list[str]): a list of urls of individual videos from the playlist if success

        Raises:
            IOError: if unable to retrive the links from the playlist

        """
        playlist = Playlist(url)
        try:
            playlist.populate_video_urls()
        except:
            raise IOError

        output = playlist.video_urls

        return output

    def printconfig(self):
        """Print the loaded config"""

        print_color(f"Local Folders: {self.localMusicFolders}")
        print_color(f"Active: {self.localMusicFoldersActive}")
        print_color(f"Youtube Playlists: {self.youtubePlaylists}")
        print_color(f"Active: {self.youtubePlaylistsActive}")
        print_color(f"Silence Interval: {self.interval}")
        print_color(f"{len(self.songfiles)} music files found.")



    def loadconfig(self):
        """Loads the configuration file"""

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
        """Fetch songs from the local music folders and Youtube playlists
        Returns: 
            An array of local files and youtube videos links
        
        """
        
        soundfiles = []

        if self.localMusicFoldersActive:
            for localMusicFolder in self.localMusicFolders:
                for fileType in self.fileTypes:
                    for filename in Path(localMusicFolder).rglob(fileType):
                        soundfiles.append(str(filename))


        if self.youtubePlaylistsActive:
            for youtubePlaylist in self.youtubePlaylists:
                
                try:
                    youtubePlaylistLinks = self.getPlaylistLinks(youtubePlaylist)
                except:
                    print("Couldn't fetch " + youtubePlaylistLinks)
                    continue

                soundfiles = soundfiles + youtubePlaylistLinks

        return soundfiles
        

    def play(self, song):
        """Instantiates a vlc player and plays a song from the list of playable songs. 
        Non blocking. Fetch and returns the title of the song if it is a Youtube song.  
        """

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
        """Pauses the player"""
        self.player.pause()

    def stop(self):
        """Stops the player"""
        self.player.stop()

    def resume(self):
        """Resumes a previously paused player"""
        self.player.play()

    def get_state(self):
        """
        Returns the state of the player:
        {0: 'NothingSpecial',
        1: 'Opening',
        2: 'Buffering',
        3: 'Playing',
        4: 'Paused',
        5: 'Stopped',
        6: 'Ended',
        7: 'Error'}
        """
        

        return self.player.get_state()


if __name__ == "__main__":
    """Tests the slothplayer module by playing and pausing a song."""

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

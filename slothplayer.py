import random, os, time, sys, vlc
from pathlib import Path
import hjson
from pytube import YouTube, Playlist
import re
import html
import threading
from colorama import Fore, Back, Style, init
from kbhit import KBHit

def printColor(text, argcolor = "white"):

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


def horizontalLine():
    printColor("--------------------------------")


def getPlaylistLinks(url):

    playlist = Playlist(url)
    playlist.populate_video_urls()

    output = playlist.video_urls

    return output



class Config():

    def __init__(self, file):
        self.loadconfig(file)

    def printconfig(self):

        printColor(f"Local Folders: {self.localMusicFolders}")
        printColor(f"Active: {self.localMusicFoldersActive}")
        printColor(f"Youtube Playlists: {self.youtubePlaylists}")
        printColor(f"Active: {self.youtubePlaylistsActive}")
        printColor(f"Silence Interval: {self.interval}")
        printColor(f"{len(self.songfiles)} music files found.")



    def loadconfig(self, file):

        while True:
            try:
                with open(file, encoding='utf-8') as config_file:
                    data = hjson.load(config_file)
                    break
            except:
                printColor("The configuration couldn't be loaded, please check the syntax of config.txt. Press any button when ready")
                os.startfile("config.txt")
                input()

        self.localMusicFolders = data['localMusicFolders']
        self.localMusicFoldersActive = data['localMusicFoldersActive']
        self.youtubePlaylists = data['youtubePlaylists']
        self.youtubePlaylistsActive = data['youtubePlaylistsActive']
        self.consecutiveReadings = data['consecutiveReadings']
        self.maxSongPlayTime = data['maxSongPlayTime']
        self.fileTypes = data['fileTypes']
        self.interval = data['interval']
        self.npressed = False
        self.songfiles = self.__getsongs()

    def __getsongs(self):
        
        soundfiles = []

        if self.localMusicFoldersActive:
            for localMusicFolder in self.localMusicFolders:
                for fileType in self.fileTypes:
                    for filename in Path(localMusicFolder).rglob(fileType):
                        soundfiles.append(str(filename))


        if self.youtubePlaylistsActive:
            for youtubePlaylist in self.youtubePlaylists:
                youtubePlaylistLinks = getPlaylistLinks(youtubePlaylist)

                soundfiles = soundfiles + youtubePlaylistLinks

        return soundfiles


    

def thread_keyboard(config):

    kb = KBHit()

    while True:
        if kb.kbhit():
            keyPressed = kb.getch()

            if keyPressed == 'n':
                config.npressed  = True

            elif keyPressed == 'c':
                horizontalLine()
                printColor("Opening configuration file")
                horizontalLine()
                os.startfile("config.txt")
            elif keyPressed == 'r':
                horizontalLine()
                printColor("Loading Config...")
                horizontalLine()
                config.loadconfig("config.txt")
                config.printconfig()
            elif keyPressed == 'q':
                horizontalLine()
                print("Goodbye", Fore.WHITE)
                os._exit(1)
            else:
                pass


        time.sleep(0.2)



if __name__ == '__main__':

    init()

    try:
        ## your code, typically one function call

        printColor('''                                                                                                                                                                                                                                                             
   _____ _       _   _       _____  _                       
  / ____| |     | | | |     |  __ \| |                      
 | (___ | | ___ | |_| |__   | |__) | | __ _ _   _  ___ _ __ 
  \___ \| |/ _ \| __| '_ \  |  ___/| |/ _` | | | |/ _ \ '__|
  ____) | | (_) | |_| | | | | |    | | (_| | |_| |  __/ |   
 |_____/|_|\___/ \__|_| |_| |_|    |_|\__,_|\__, |\___|_|   
                                             __/ |          
                                            |___/                          
 v1-beta
        ''', "magenta")



        horizontalLine()
        printColor("Loading Config...")
        horizontalLine()
        config = Config("config.txt")

        config.printconfig()


        instance=vlc.Instance("--novideo", "--verbose=0")
        player=instance.media_player_new()

        x = threading.Thread(target=thread_keyboard, args=(config,), daemon=True)
        x.start()



        songsPlayed = 0

        while True: # main loop (each song)

            horizontalLine()
            song = random.choice(config.songfiles)

            song_title = ''
            if re.search('youtube.com', song):
                song_title = html.unescape(YouTube(song).title)
                

            
            # song ="https://youtu.be/9U-N6LqzdIM"


            media = instance.media_new(song)

            # song is the YouTube or a local URL

            media_list = instance.media_list_new([song]) #A list of one song

            player = instance.media_player_new()
            player.set_media(media)

            # Create a new MediaListPlayer instance and associate the player and playlist with it
            list_player =  instance.media_list_player_new()
            list_player.set_media_player(player)
            list_player.set_media_list(media_list)

            player.audio_set_volume(100)
            player.play()

            playing = set([1,2,3,4])
            
            # Song loading management
            i = 0
            while i < 10:
                time.sleep(1) #Give time to get going
                duration = player.get_length() / 1000
                mm, ss = divmod(duration, 60)
                if mm+ss == 0: # means song not loaded
                    i = i+1
                else:
                    break

            if i == 10:
                printColor("Song couldn't be loaded, next...")
                continue

            # the song has loaded at this point
            songStartTime = time.time()
            

            if song_title != '': 
                printColor(f"Playing: {song_title} Length: {mm:00.0f}:{ss:00.0f}", "green")
                printColor(song, 'green')
            else:
                printColor(f"Playing: {song} Length: {mm:00.0f}:{ss:00.0f}", "green")
                pass


            printColor("Press (n) to skip, (c) to open config.txt, (r) to reload configuration and (q) to quit", "pink")


            while True: # loop while playing, waiting for user input

                # stop song if it is too long
                if time.time() - songStartTime > config.maxSongPlayTime * 60:
                    printColor(f"Song exceeded max allowed duration ({config.maxSongPlayTime} minutes). Stoping...")
                    
                    #fade out
                    for i in range(100,0,-5):
                        player.audio_set_volume(i)
                        time.sleep(0.5)

                    player.stop()
                
                # stop song if user request
                # if kb.kbhit():
                #     if kb.getch() == 'n':
                #         print("Next song...")
                #         player.stop()
                #         break  # finishing the loop

                #     else:
                #         pass

                if config.npressed == True:
                    config.npressed = False
                    horizontalLine()
                    printColor("Next song...")
                    player.stop()
                    break  # finishing the loop



                state = player.get_state()
                # print(state)

                if state not in playing: # if the song is finished

                    songsPlayed += 1 # increase counter of songs played

                    if songsPlayed < config.consecutiveReadings:
                        #read another song
                        break
                    else:
                        #wait the required sleep interval
                        sleepInterval = random.randint(config.interval[0],config.interval[1])

                        printColor(f'Sleeping for {sleepInterval} minutes')
                        printColor("Press (n) to skip, (c) to open config.txt, (r) to reload configuration and (q) to quit", "pink")


                        for i in range(sleepInterval*60,0,-1):
                                
                            if config.npressed == True:
                                config.npressed = False
                                horizontalLine()
                                printColor("Next song...")
                                player.stop()
                                break  # finishing the loop


                            if i%60 == 0:
                                sys.stdout.write(str(int(i/60))+' ')
                                sys.stdout.flush()

                            time.sleep(1)

                        print(' ')

                        # end of cycle, reset number of songs played
                        songsPlayed = 0

                        break

                time.sleep(1)



    except BaseException: # to keep the command window open upon exit (in case of error for example)
        import sys
        printColor(sys.exc_info()[0])
        import traceback
        printColor(traceback.format_exc())
    finally:
        print("Press Enter to continue ...", Fore.WHITE)
        input()

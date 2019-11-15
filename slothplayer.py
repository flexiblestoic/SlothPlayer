import random, os, time, sys, vlc
import msvcrt
from pathlib import Path
import hjson
from bs4 import BeautifulSoup
import requests


def horizontalLine():
    print("##############################################")

def getPlaylistLinks(url):
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'

    output = []
    playlistData = {}

    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            # print(link.string.strip())
            pathToVideo = domain + href
            output.append(pathToVideo)
            playlistData[pathToVideo] = link.string.strip()

    return output, playlistData


def loadConfig():
    with open('config.txt', encoding='utf-8') as config_file:
        data = hjson.load(config_file)
    return data


if __name__ == '__main__':
    try:
        ## your code, typically one function call

        print('''                                                                                                                                                                                                                                                             
   _____ _       _   _       _____  _                       
  / ____| |     | | | |     |  __ \| |                      
 | (___ | | ___ | |_| |__   | |__) | | __ _ _   _  ___ _ __ 
  \___ \| |/ _ \| __| '_ \  |  ___/| |/ _` | | | |/ _ \ '__|
  ____) | | (_) | |_| | | | | |    | | (_| | |_| |  __/ |   
 |_____/|_|\___/ \__|_| |_| |_|    |_|\__,_|\__, |\___|_|   
                                             __/ |          
                                            |___/                          
 v1-beta
        ''')



        horizontalLine()
        print("Loading Config...")

        data = loadConfig()

        localMusicFolders = data['localMusicFolders']
        localMusicFoldersActive = data['localMusicFoldersActive']
        youtubePlaylists = data['youtubePlaylists']
        youtubePlaylistsActive = data['youtubePlaylistsActive']
        consecutiveReadings = data['consecutiveReadings']
        fileTypes = data['fileTypes']
        interval = data['interval']

        print(f"Local Folders: {localMusicFolders}")
        print(f"Active: {localMusicFoldersActive}")
        print(f"Youtube Playlists: {youtubePlaylists}")
        print(f"Active: {youtubePlaylistsActive}")
        print(f"Silence Interval: {interval}")

        instance=vlc.Instance("--novideo", "--verbose=0")
        player=instance.media_player_new()

        # os.system('cls' if os.name == 'nt' else 'clear')
        horizontalLine()
        print("Searching for music...")

        # populate soundfiles and playlists
        soundfiles = []
        if localMusicFoldersActive:
            for localMusicFolder in localMusicFolders:
                for fileType in fileTypes:
                    for filename in Path(localMusicFolder).rglob(fileType):
                        soundfiles.append(str(filename))


        playlistData = {}

        if youtubePlaylistsActive:
            for youtubePlaylist in youtubePlaylists:

                youtubePlaylistLinks, playlistDataTemp = getPlaylistLinks(youtubePlaylist)

                for youtubePlaylistLink in youtubePlaylistLinks:
                    soundfiles.append(youtubePlaylistLink)

                playlistData.update(playlistDataTemp)


        # print(soundfiles)

        print(f"{len(soundfiles)} music files found.")

        songsPlayed = 0

        while True: # main loop (each song)

            horizontalLine()
            song = random.choice(soundfiles)
            
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
                print("Song couldn't be loaded, next...")
                continue

            if playlistData.get(song, None) != None: # attempts to find title for youtube songs
                print("Playing:", playlistData[song], "Length:", "%02d:%02d" % (mm,ss))
                print(song)
            else:
                print("Playing:", song, "Length:", "%02d:%02d" % (mm,ss))


            print("Press (n) to next")


            while True: # loop while playing, waiting for user input
                    
                if msvcrt.kbhit():
                    if msvcrt.getch() == b'n':
                        print("Next song...")
                        player.stop()
                        break  # finishing the loop

                    else:
                        pass


                state = player.get_state()
                # print(state)

                if state not in playing: # if the song is finished

                    player.stop() #for safety, let's make sure to close the instance, to not have 2 running

                    songsPlayed += 1 # increase counter of songs played

                    if songsPlayed < consecutiveReadings:
                        #read another song
                        break
                    else:
                        #wait the required sleep interval
                        sleepInterval = random.randint(interval[0],interval[1])

                        print(f'Sleeping for {sleepInterval} minutes')
                        print("Press (n) to skip pause")


                        for i in range(sleepInterval*60,0,-1):
                            if msvcrt.kbhit():
                                if msvcrt.getch() == b'n':
                                    print("Skip pause...")
                                    break  # finishing the loop

                                else:
                                    pass


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
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("Press Enter to continue ...")
        input()

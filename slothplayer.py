import random, os, time, sys, vlc
from pathlib import Path
import hjson
from pytube import YouTube, Playlist
import re
import html
import threading

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit: #non blocking io from https://stackoverflow.com/questions/2408560/python-nonblocking-console-input

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []



def horizontalLine():
    print("##############################################")


def getPlaylistLinks(url):

    playlist = Playlist(url)
    playlist.populate_video_urls()

    output = playlist.video_urls

    return output



class Config():

    def __init__(self, file):
        self.loadconfig(file)

    def loadconfig(self, file):

        # try:
        #     config = loadConfig("config.txt")
        # except:
        #     print("The configuration couldn't be loaded, please check the syntax of config.txt")
        #     sys.exit(1)

        with open(file, encoding='utf-8') as config_file:
            data = hjson.load(config_file)

        self.localMusicFolders = data['localMusicFolders']
        self.localMusicFoldersActive = data['localMusicFoldersActive']
        self.youtubePlaylists = data['youtubePlaylists']
        self.youtubePlaylistsActive = data['youtubePlaylistsActive']
        self.consecutiveReadings = data['consecutiveReadings']
        self.maxSongPlayTime = data['maxSongPlayTime']
        self.fileTypes = data['fileTypes']
        self.interval = data['interval']
        self.npressed = False

    def getsongs(self):
        
        soundfiles = []

        if self.localMusicFoldersActive:
            for localMusicFolder in self.localMusicFolders:
                for fileType in self.fileTypes:
                    for filename in Path(localMusicFolder).rglob(fileType):
                        soundfiles.append(str(filename))


        if self.youtubePlaylistsActive:
            for youtubePlaylist in self.youtubePlaylists:
                youtubePlaylistLinks = getPlaylistLinks(youtubePlaylist)

                for youtubePlaylistLink in youtubePlaylistLinks:
                    soundfiles.append(youtubePlaylistLink)

        return soundfiles


    

def thread_keyboard(config):

    kb = KBHit()

    while True:
        if kb.kbhit():
            keyPressed = kb.getch()

            if keyPressed == 'n':
                config.npressed  = True

            elif keyPressed == 'c':
                print("Opening configuration file")
                os.startfile("config.txt")
            elif keyPressed == 'r':
                config.reloadconfig("config.txt")
                print("Configuration reloaded")
            else:
                pass


        time.sleep(0.2)



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

        config = Config("config.txt")


        print(f"Local Folders: {config.localMusicFolders}")
        print(f"Active: {config.localMusicFoldersActive}")
        print(f"Youtube Playlists: {config.youtubePlaylists}")
        print(f"Active: {config.youtubePlaylistsActive}")
        print(f"Silence Interval: {config.interval}")

        instance=vlc.Instance("--novideo", "--verbose=0")
        player=instance.media_player_new()

        x = threading.Thread(target=thread_keyboard, args=(config,), daemon=True)
        x.start()


        # os.system('cls' if os.name == 'nt' else 'clear')
        horizontalLine()
        print("Searching for music...")



        print(f"{len(config.getsongs())} music files found.")

        songsPlayed = 0

        while True: # main loop (each song)



            horizontalLine()
            song = random.choice(config.getsongs())

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
                print("Song couldn't be loaded, next...")
                continue

            # the song has loaded at this point
            songStartTime = time.time()
            

            if song_title != '': 
                print("Playing:", song_title, "Length:", "%02d:%02d" % (mm,ss))
                print(song)
            else:
                print("Playing:", song, "Length:", "%02d:%02d" % (mm,ss))


            print("Press (n) to next")


            while True: # loop while playing, waiting for user input

                # stop song if it is too long
                if time.time() - songStartTime > config.maxSongPlayTime * 60:
                    print(f"Song exceeded max allowed duration ({config.maxSongPlayTime} minutes). Stoping...")
                    
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
                    print("Next song...")
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

                        print(f'Sleeping for {sleepInterval} minutes')
                        print("Press (n) to skip pause")


                        for i in range(sleepInterval*60,0,-1):
                                
                            if config.npressed == True:
                                config.npressed = False
                                print("Next song...")
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

        kb.set_normal_term()

    except BaseException: # to keep the command window open upon exit (in case of error for example)
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("Press Enter to continue ...")
        input()

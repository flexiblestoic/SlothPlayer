import random, os, time, sys
import threading
from kbhit import KBHit
from colorama import Fore, Back, Style, init
from slothplayer import printColor, SlothPlayer
import logging

#logging.basicConfig(level=logging.DEBUG)

CONFIGURATION_FILE = "config.txt"

def horizontalLine():
    printColor("--------------------------------")


def thread_keyboard(slothplayer):

    kb = KBHit()

    while True:
        if kb.kbhit():
            keyPressed = kb.getch()

            if keyPressed == 'n':
                slothplayer.npressed  = True

            elif keyPressed == 'c':
                horizontalLine()
                printColor("Opening configuration file")
                horizontalLine()
                os.startfile(slothplayer.configuration_file)
            elif keyPressed == 'r':
                horizontalLine()
                printColor("Loading Config...")
                horizontalLine()
                slothplayer.loadconfig()
                slothplayer.printconfig()
            elif keyPressed == 'q':
                horizontalLine()
                print("Goodbye", Fore.WHITE)
                printColor(f"Run Time: {time.strftime('%H:%M:%S', time.gmtime(time.time()-slothplayer.init_time))}")
                os._exit(1)
            elif keyPressed == 'p':
                slothplayer.ppressed  = True
            else:
                pass


        time.sleep(0.2)


def initialize_player(config_file, auto_open=True):
    
    init()
    printColor(r'''                                                                                                                                                                                                                                                             
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
    slothplayer = SlothPlayer(config_file)

    printColor(f"Start Time: {time.strftime('%H:%M:%S', time.localtime(slothplayer.init_time))}")
    horizontalLine()

    while True:
        try:
            slothplayer.loadconfig()
            slothplayer.printconfig()

            x = threading.Thread(target=thread_keyboard, args=(slothplayer,), daemon=True)
            x.start()

            break


        except:
            printColor("The configuration couldn't be loaded, please check the syntax of config.txt. Press any button when ready")
            if auto_open == True:
                os.startfile(config_file)
                input()
            else:
                raise IOError("Couldn't open the configuration file")
                


    return slothplayer

    

def play_song(slothplayer, song):

    #Plays a song and return to main thread when the song is over or upon user intervention

    logging.debug('Fetching song title')
    try:
        song_title = slothplayer.play(song)
    except:
        return False

    
    logging.debug('Fetching song title... done')

    playing = set([1,2,3,4])
    
    # Song loading management
    i = 0
    while i < 10:
        time.sleep(1) #Give time to get going
        duration = slothplayer.player.get_length() / 1000
        mm, ss = divmod(duration, 60)
        if mm+ss == 0: # means song not loaded
            i = i+1
        else:
            break

    if i == 10:
        printColor("Song couldn't be loaded, next...")
        return False

    # the song has loaded at this point
    songStartTime = time.time()
    
    if song_title == "":
        printColor(f"Playing: {song} Length: {mm:00.0f}:{ss:00.0f}", "green")
    else:
        printColor(f"Playing: {song_title} Length: {mm:00.0f}:{ss:00.0f}", "green")
        printColor(song, "green")

    printColor("Press (n) to skip, (p) to pause, (c) to open " + slothplayer.configuration_file +  ", (r) to reload configuration and (q) to quit", "pink")

    logging.debug('Playing, waiting for user input')

    while True: # loop while playing, waiting for user input
        # stop song if it is too long
        logging.debug('stop song if it is too long')
        if time.time() - songStartTime > slothplayer.maxSongPlayTime * 60:
            printColor(f"Song exceeded max allowed duration ({slothplayer.maxSongPlayTime} minutes). Stoping...")
            
            #fade out
            for i in range(100,0,-5):
                slothplayer.player.audio_set_volume(i)
                time.sleep(0.5)

            slothplayer.stop()

        logging.debug('if slothplayer.npressed == True:')
        if slothplayer.npressed == True:
            slothplayer.npressed = False
            horizontalLine()
            printColor("Next song...")
            slothplayer.stop()
            break  # finishing the loop
        
        logging.debug('if slothplayer.ppressed == True:')
        if slothplayer.ppressed == True:
            slothplayer.ppressed = False
            horizontalLine()
            printColor("Pause... Press Enter to continue")
            horizontalLine()
            slothplayer.pause()

            pause_duration = pause_program()

            songStartTime += pause_duration # offset music time by time spent in pause
            slothplayer.resume()
            
        logging.debug('state = slothplayer.get_state()')
        state = slothplayer.get_state()
        # print(state)

        if state not in playing: # if the song is finished
            
            logging.debug('State not in playing')
            return time.time()-songStartTime



def play_silence(slothplayer, sleepInterval):

    for i in range(sleepInterval*60*slothplayer.refreshFrequency,0,-1):
                        
        if slothplayer.npressed == True:
            slothplayer.npressed = False
            horizontalLine()
            printColor("Next song...")
            slothplayer.stop()
            break  # finishing the loop


        if slothplayer.ppressed == True:
            slothplayer.ppressed = False
            horizontalLine()
            printColor("Pause... Press Enter to continue")
            horizontalLine()

            pause_program()


        if i%(60*slothplayer.refreshFrequency) == 0:
            sys.stdout.write(str(int(i/(60*slothplayer.refreshFrequency)))+' ')
            sys.stdout.flush()

        time.sleep(1.0/slothplayer.refreshFrequency)


def pause_program():
    
    pause_start_time = time.time()
    input()
    pause_duration = time.time() - pause_start_time

    return pause_duration

if __name__ == '__main__':


    try:

        slothplayer = initialize_player(CONFIGURATION_FILE)

        while True: # main loop (each song)

            logging.debug('In main loop')
            horizontalLine()

            song = random.choice(slothplayer.songfiles)

            if play_song(slothplayer, song):
                slothplayer.songs_played += 1 # increase counter of songs played
            else:
                continue

            if slothplayer.songs_played < slothplayer.consecutiveReadings:
                #read another song
                break
            else:
                #wait the required sleep interval
                sleepInterval = random.randint(slothplayer.interval[0],slothplayer.interval[1])
                printColor(f'Sleeping for {sleepInterval} minutes')
                printColor("Press (n) to skip, (p) to pause, (c) to open " + slothplayer.configuration_file +  ", (r) to reload configuration and (q) to quit", "pink")

                play_silence(slothplayer, sleepInterval)
                print(' ')

                # end of cycle, reset number of songs played
                slothplayer.songs_played = 0
                break

        time.sleep(1.0/slothplayer.refreshFrequency)


    except BaseException: # to keep the command window open upon exit (in case of error for example)
        import sys
        printColor(sys.exc_info()[0])
        import traceback
        printColor(traceback.format_exc())

    finally:
        print("Press Enter to continue ...", Fore.WHITE)
        input()

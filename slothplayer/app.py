import random, os, time, sys, math
import threading
from slothplayer.tools import KBHit, print_color, init, Fore
from slothplayer.slothplayer import SlothPlayer
import logging

#logging.basicConfig(level=logging.DEBUG)

CONFIGURATION_FILE = "config.txt"

def horizonta_line():
    print_color("--------------------------------")


def thread_keyboard(slothplayer):
    """
    Non blocking thread for the keyboard inputs which either acts or writes flags for the main thread

    """
    kb = KBHit()

    while True:
        if kb.kbhit():
            key_pressed = kb.getch()

            if key_pressed == 'n':
                slothplayer.npressed  = True

            elif key_pressed == 'c':
                horizonta_line()
                print_color("Opening configuration file")
                horizonta_line()
                os.startfile(slothplayer.configuration_file)
            elif key_pressed == 'r':
                horizonta_line()
                print_color("Loading Config...")
                horizonta_line()
                slothplayer.loadconfig()
                slothplayer.printconfig()
            elif key_pressed == 'q':
                horizonta_line()
                print_color(f"Run Time: {time.strftime('%H:%M:%S', time.gmtime(time.time()-slothplayer.init_time))}")
                print(" Goodbye", Fore.WHITE)
                input()
                os._exit(1)
            elif key_pressed == 'p':
                slothplayer.ppressed  = True
            else:
                pass


        time.sleep(0.2)


def initialize_player(config_file, auto_open=True):
    """
    Initializes the vlc player, loads config and the playlists.
    """
    init()
    print_color(r'''                                                                                                                                                                                                                                                             
   _____ _       _   _       _____  _                       
  / ____| |     | | | |     |  __ \| |                      
 | (___ | | ___ | |_| |__   | |__) | | __ _ _   _  ___ _ __ 
  \___ \| |/ _ \| __| '_ \  |  ___/| |/ _` | | | |/ _ \ '__|
  ____) | | (_) | |_| | | | | |    | | (_| | |_| |  __/ |   
 |_____/|_|\___/ \__|_| |_| |_|    |_|\__,_|\__, |\___|_|   
                                             __/ |          
                                            |___/                          
 v1.0-beta
    ''', "green")



    horizonta_line()
    print_color("Loading Config...")
    horizonta_line()
    slothplayer = SlothPlayer(config_file)

    print_color(f"Start Time: {time.strftime('%H:%M:%S', time.localtime(slothplayer.init_time))}")
    horizonta_line()

    while True:
        try:
            slothplayer.loadconfig()
            slothplayer.printconfig()

            x = threading.Thread(target=thread_keyboard, args=(slothplayer,), daemon=True)
            x.start()

            break


        except:
            print_color("The configuration couldn't be loaded, please check the syntax of config.txt. Press any button when ready")
            if auto_open == True:
                os.startfile(config_file)
                input()
            else:
                raise IOError("Couldn't open the configuration file or Youtube playlist")
                


    return slothplayer

    

def play_song(slothplayer, song):
    """
    Plays a song and stops when the song finished playing or if the player failed. The user can interrupt with a (n) press or pause with a (p) press.
    Returns:
        False if no song could be played.
        Duration of the song if it was played.
    """
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
        print_color("Song couldn't be loaded, next...")
        return False

    # the song has loaded at this point
    songStartTime = time.time()
    
    if song_title == "":
        print_color(f"Playing: {song} Length: {mm:00.0f}:{ss:00.0f}", "green")
    else:
        print_color(f"Playing: {song_title} Length: {mm:00.0f}:{ss:00.0f}", "green")
        print_color(song, "green")

    print_color("Press (n) to skip, (p) to pause, (c) to open " + slothplayer.configuration_file +  ", (r) to reload configuration and (q) to quit", "pink")

    logging.debug('Playing, waiting for user input')

    while True: # loop while playing, waiting for user input
        # stop song if it is too long
        logging.debug('stop song if it is too long')
        if time.time() - songStartTime > slothplayer.maxSongPlayTime * 60:
            print_color(f"Song exceeded max allowed duration ({slothplayer.maxSongPlayTime} minutes). Stoping...")
            
            #fade out
            for i in range(100,0,-5):
                slothplayer.player.audio_set_volume(i)
                time.sleep(0.5)

            slothplayer.stop()

        logging.debug('if slothplayer.npressed == True:')
        if slothplayer.npressed == True:
            slothplayer.npressed = False
            horizonta_line()
            print_color("Next song...")
            slothplayer.stop()
            break  # finishing the loop
        
        logging.debug('if slothplayer.ppressed == True:')
        if slothplayer.ppressed == True:
            slothplayer.ppressed = False
            horizonta_line()
            print_color("Pause... Press Enter to continue")
            horizonta_line()
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

        time.sleep(1.0/slothplayer.refreshFrequency)



def play_silence(slothplayer, sleepInterval):
    """
    Plays silence. The user can interrupt with a (n) press or pause with a (p) press.

    Returns:
        Duration of silence
    """
    start_silence_time = time.time()

    for i in range(math.floor(sleepInterval*60*slothplayer.refreshFrequency),0,-1):
                        
        if slothplayer.npressed == True:
            slothplayer.npressed = False
            horizonta_line()
            print_color("Next song...")
            slothplayer.stop()
            break  # finishing the loop


        if slothplayer.ppressed == True:
            slothplayer.ppressed = False
            print("")
            horizonta_line()
            print_color("Pause... Press Enter to continue")
            horizonta_line()

            pause_program()


        if i%(60*slothplayer.refreshFrequency) == 0:
            sys.stdout.write(' ' + str(int(i/(60*slothplayer.refreshFrequency))))
            sys.stdout.flush()

        time.sleep(1.0/slothplayer.refreshFrequency)

    return time.time()-start_silence_time


def pause_program():
    """
    Pauses the execution. Resumes when user presses enter.

    Returns:
        Pause duration
    """
    pause_start_time = time.time()
    input()
    pause_duration = time.time() - pause_start_time

    return pause_duration

def app():

    """
    Main loop. Plays a number of songs per the config. Waits for a duration of silence per the config. 
    """


    try:

        slothplayer = initialize_player(CONFIGURATION_FILE)

        while True: # main loop (each song)

            logging.debug('In main loop')
            horizonta_line()

            song = random.choice(slothplayer.songfiles)

            if play_song(slothplayer, song):
                slothplayer.songs_played += 1 # increase counter of songs played
            else:
                continue

            if slothplayer.songs_played < slothplayer.consecutiveReadings:
                #read another song
                continue
            else:
                #wait the required sleep interval
                sleepInterval = random.randint(slothplayer.interval[0],slothplayer.interval[1])
                print_color(f'Sleeping for {sleepInterval} minutes')
                print_color("Press (n) to skip, (p) to pause, (c) to open " + slothplayer.configuration_file +  ", (r) to reload configuration and (q) to quit", "pink")

                play_silence(slothplayer, sleepInterval)
                print(' ')

                # end of cycle, reset number of songs played
                slothplayer.songs_played = 0

            time.sleep(1.0/slothplayer.refreshFrequency)


    except BaseException: # to keep the command window open upon exit (in case of error for example)
        import sys
        print_color(sys.exc_info()[0])
        import traceback
        print_color(traceback.format_exc())

    finally:
        print("Press Enter to continue ...", Fore.WHITE)
        input()


if __name__ == "__main__":
    app()
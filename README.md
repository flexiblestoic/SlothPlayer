# Sloth Player
A music and silence player

## Why?
Don't you sometimes wish you could find the ideal balance between music and silence? This is exactly what Sloth Player has been created for. It is a jukebox where you can also configure the pause between the tracks.

## Is it free and open source?
Yes. The player is built on top of python, python-vlc, pytube and vlc, amongst other open source software. 

## How can I be sure it is safe?
It is open source so you can clone the repository and install it on any system with python running. For the app to work reliably, please copy *.dll at the base of the vlc installation into the root of the python app as well as the lua and plugins folder.  
The executable can be scanned with an antivirus.

## What can it do?
Can play local files and Youtube in a random setting. You can configure how many songs the jukebox plays in one go and how long you want the player to pause between two bursts of songs.  
Supported formats: all formats supported by vlc (incl. mp3, aac, flac, wma)

## How does it work?
First download the program on the Github release page:  https://github.com/flexiblestoic/SlothPlayer/releases

Then you need to edit the configuration file config.txt. The config file's format is hjson https://hjson.org/ which is slightly different than json (more readable). In particular comments are allowed `#` and end of line commas are not compulsory. Hence, `#` can be conveniently used to write reminders in the configuration file or temporarily remove a line/playlist. 

And that is pretty much it!

**localMusicFolders**: (path) local folders to be scanned
**localMusicFoldersActive**: (true/false) activate or not the local mode

**youtubePlaylists**: (path) youtube playlists to be scanned
**youtubePlaylistsActive**: (true/false) activate or not the youtube mode

**consecutiveReadings**: (integer) number of songs to be read before silence

**maxSongPlayTime**: (integer) max duration of a song in minutes before it is faded out and next song is played

**fileTypes**: (file types) types of files to take into account

**interval**: (integers) min and max number of minutes of silence between 2 tracks (the application with choose a random number between the lower and upper limits)

**Example:** 

```
{
  "localMusicFolders": [
    #"C:\\music"
    #"D:\\mymusic"
  ]

  "localMusicFoldersActive": true

  "youtubePlaylists": [
    #"https://www.youtube.com/playlist?list=PLo3pNg0eiPc-9livXsto4X1ROzJ3kGI-3"  # Quiet Songs Playlist 2020
    #"https://www.youtube.com/playlist?list=PLd6-Jg5IeeosymMDHA5QhzA2CbelAGN6e" # Accoustic
    #"https://www.youtube.com/playlist?list=PLw9zKTSWmoixGTX-e8y0R6xkF6Eq1RhEZ" # Chillhop
    "https://www.youtube.com/playlist?list=PLd3udltX2Fih-fkvfbw0zENvao9bm8Awh" # Post Modern Jukebox (the only one selected in this config.txt)
    #"https://www.youtube.com/playlist?list=PLyvDPG7a_zWCf7tiyWqNBKynAi0_7I-Nr"# Adagios Classical Music
  ]

  "youtubePlaylistsActive": true

  "consecutiveReadings": 2

  "maxSongPlayTime": 10

  "interval": [4, 7]

  "fileTypes": ["*.mp3", "*.wma", "*.flac", "*.aac", "*.ogg"]
}
```

**Keyboard controls during play:**
Press (n) to skip, (p) to pause, (c) to open the configuration file, (r) to reload configuration after change and (q) to quit.

## Which platform?
The code is a python code which is compatible with multiple platforms. However, I have only tested and compiled a binary version for Windows x64. Please let me know if you are able to run on MacOS/Linux and are interested in submitting a compiled version for those platforms.

## Credits
logo: http://pngimg.com/download/71212
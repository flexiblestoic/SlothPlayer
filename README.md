# Sloth Player
A music and silence player

## Why?
Don't you sometimes wish you could find the ideal balance between music and silence? This is exactly what Sloth Player has been created for. It is a jukebox where you can also configure the pause between the tracks.

## Is it free and open source?
Yes, and open source too. The player is built on top of python, python-vlc and vlc, amongst other open source software. 

## What can it do?
Can play local files and Youtube in a random setting. You can configure how long you want the player to pause between two tracks.
Supported formats: all formats supported by vlc (incl. mp3, aac, flac, wma)

## How does it work?
First, you need to edit the configuration file config.txt. The config file's format is hjson [https://hjson.org/]

localMusicFolders: (path) local folders to be scanned
localMusicFoldersActive: (true/false) activate or not the local mode

youtubePlaylists: (path) youtube playlists to be scanned
youtubePlaylistsActive: (true/false) activate or not the youtube mode

consecutiveReadings: (integer) number of songs to be read before silence

fileTypes: (file types) types of files to take into account

interval: (integers) min and max number of minutes of silence between 2 tracks (the application with choose a random number between the lower and upper limits)

Example: 

```hjson
{
  "localMusicFolders": [
    "C:\\music"
    "D:\\mymusic"
  ]

  "localMusicFoldersActive": false

  "youtubePlaylists": [
    "https://www.youtube.com/playlist?list=PLo3pNg0eiPc-9livXsto4X1ROzJ3kGI-3"  # Quiet Songs Playlist 2020
    "https://www.youtube.com/playlist?list=PLd6-Jg5IeeosymMDHA5QhzA2CbelAGN6e" # Accoustic
  ]

  "youtubePlaylistsActive": true

  "consecutiveReadings": 2

  "fileTypes": ["*.mp3", "*.wma", "*.flac", "*.aac", "*.ogg"]
  "interval": [4, 7]
}
```

## Which platform?
The code is a python code which is compatible with multiple platforms. However, I have only tested and compiled a binary version for Windows x64. Please let me know if you are able to run on MacOS/Linux and are interested in submitting a compiled version for those platforms.

# Credits
logo: http://pngimg.com/download/71212
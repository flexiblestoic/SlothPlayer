import pytest
from slothplayer.slothplayer import SlothPlayer

@pytest.fixture
def load_good_config():
    return ".\\tests\\mocks\\goodconfig.txt"


@pytest.fixture
def load_bad_config():
    return ".\\tests\\mocks\\badonfig.txt"


def test_good_config(load_good_config):
    sloth = SlothPlayer(load_good_config)
    sloth.loadconfig()
    assert sloth.interval == [4,7]

def test_bad_config(load_bad_config):
    sloth = SlothPlayer(load_bad_config)
    with pytest.raises(IOError):
        sloth.loadconfig()

from slothplayer.app import initialize_player
def test_initialize_player_good(load_good_config):
    sloth = initialize_player(load_good_config, False)
    assert sloth.interval == [4,7]

def test_initialize_player_bad(load_bad_config):
        with pytest.raises(IOError):
            sloth = initialize_player(load_bad_config, False)

from slothplayer.app import play_silence
def test_play_silence(load_good_config):
    slothplayer = SlothPlayer(load_good_config)
    slothplayer.loadconfig()
    actual_silence = play_silence(slothplayer, 0.03333) # 2 seconds
    assert abs(actual_silence - 2) < 0.2

from slothplayer.app import play_song
def test_play_song_good(load_good_config):
    slothplayer = SlothPlayer(load_good_config)
    slothplayer.loadconfig()
    result = play_song(slothplayer, "https://www.youtube.com/watch?v=PCicKydX5GE")
    assert abs(result - 3) < 1


def test_play_song_bad(load_good_config):
    slothplayer = SlothPlayer(load_good_config)
    slothplayer.loadconfig()
    result = play_song(slothplayer, "https://www.youtube.com/watch?v=PCicKydXE")
    assert result == False 
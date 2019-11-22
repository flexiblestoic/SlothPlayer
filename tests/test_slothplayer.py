import pytest
from slothplayer import SlothPlayer

@pytest.fixture
def load_good_config():
    return ".\\tests\\mocks\\goodconfig.txt"


@pytest.fixture
def load_bad_config():
    return ".\\tests\\mocks\\badonfig.txt"


def test_good_config(load_good_config):
    sloth = SlothPlayer()
    sloth.loadconfig(load_good_config)
    assert sloth.interval == [4,7]

def test_bad_config(load_bad_config):
    sloth = SlothPlayer()
    with pytest.raises(IOError):
        sloth.loadconfig(load_bad_config)

from app import initialize_player
def test_initialize_player_good(load_good_config):
    sloth = initialize_player(load_good_config, False)
    assert sloth.interval == [4,7]

def test_initialize_player_bad(load_bad_config):
        with pytest.raises(IOError):
            sloth = initialize_player(load_bad_config, False)
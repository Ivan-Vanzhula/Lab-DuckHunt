import pytest
import DuckHunt


# Fixture to initialize a Game instance for testing
@pytest.fixture
def game_instance():
    return DuckHunt.Game()


# Test case for initializing the Game instance
def test_game_initialization(game_instance):
    assert game_instance.playing == False
    assert game_instance.menuCounter == 0
    assert game_instance.spawnCounter == 0


# Test case for spawning ducks in the game
def test_ducks_spawning(game_instance):
    game_instance.spawn()
    assert DuckHunt.GameScores.totalDucks == 1


# Test case for updating game counters
def test_game_counters(game_instance):
    game_instance.started = True

    game_instance.tick()
    assert game_instance.menuCounter == 2

    game_instance.playing = True

    game_instance.tick()
    assert game_instance.spawnCounter == 1

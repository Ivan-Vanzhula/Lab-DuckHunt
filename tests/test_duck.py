import pytest
import DuckHunt


# Fixture to initialize a Duck instance for testing
@pytest.fixture
def duck_instance():
    return DuckHunt.Duck(1)


# Test case for initializing the Duck instance
def test_duck_initialization(duck_instance):
    assert duck_instance.points == 75
    assert duck_instance.alive == True


# Test case for duck dying after being shot
def test_duck_die(duck_instance):
    duck_instance.shot()
    assert duck_instance.alive == False


# Test case for updating the duck's animation
def test_duck_animation(duck_instance):
    duck_instance.update_animation()
    assert duck_instance.animationCount == 1


# Test case for updating the duck's position and direction
def test_duck_update(duck_instance):
    duck_instance.update()
    assert duck_instance.directionCount == 1
    assert duck_instance.dy == -1

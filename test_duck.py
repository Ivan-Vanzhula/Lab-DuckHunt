import pytest
import DuckHunt

@pytest.fixture
def duck_instance():
    return DuckHunt.Duck(1)

def test_duck_initialization(duck_instance):
    assert duck_instance.points == 75
    assert duck_instance.alive == True

def test_duck_die(duck_instance):
    duck_instance.shot()

    assert duck_instance.alive == False

def test_duck_animation(duck_instance):
    duck_instance.update_animation()

    assert duck_instance.animationCount == 1

def test_duck_update(duck_instance):
    duck_instance.update()

    assert duck_instance.directionCount == 1
    assert duck_instance.dy == -1
import pytest
import DuckHunt

# Fixture to initialize a Clock instance for testing
@pytest.fixture
def clock_instance():
    return DuckHunt.Clock()


# Test case for initializing the Clock instance
def test_clock_initialization(clock_instance):
    assert clock_instance.seconds == 30
    assert clock_instance.clockCount == 0
    assert clock_instance.started == False


# Test case for starting the clock
def test_clock_start(clock_instance):
    clock_instance.start_clock()
    assert clock_instance.started == True


# Test case for updating the clock label
def test_clock_label(clock_instance):
    clock_instance.update_clock()
    assert clock_instance.timer.value == "0:30"


# Test case for ticking the clock
def test_clock_timers(clock_instance):
    clock_instance.started = True
    clock_instance.tick()
    assert clock_instance.clockCount == 1

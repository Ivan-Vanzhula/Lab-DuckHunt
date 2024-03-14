import pytest
import DuckHunt

# Fixture to initialize a Menu instance for testing
@pytest.fixture
def menu_instance():
    return DuckHunt.Menu()

# Test case for initializing the Menu instance
def test_menu_initialization(menu_instance):
    assert menu_instance.activeMenu == 0
    assert menu_instance.moveCounter == 0

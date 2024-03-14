import pytest
import DuckHunt

# Fixture to initialize a Cursor instance for testing
@pytest.fixture
def cursor_instance():
    return DuckHunt.Cursor()

# Test case for initializing the Cursor instance
def test_cursor_initialization(cursor_instance):
    assert cursor_instance.mouseClicked == False
    assert cursor_instance.mouseCounter == 0

# Test case for updating the cursor position
def test_cursor_position(cursor_instance):
    cursor_instance.update()

    assert cursor_instance.x == DuckHunt.Cursor.xPos
    assert cursor_instance.y == DuckHunt.Cursor.yPos

import pytest
import numpy as np

from .snake import Snake


@pytest.fixture
def unSnake():
    #position (2,6)
    snake=Snake(1540)
    return snake


def test_mv_up(unSnake):
    snake=unSnake
    snake.mv_up()
    assert snake.position[1] == 7
    
    snake.position =np.array([5,0])
    snake.mv_up()
    assert snake.alive

    snake.alive=True
    snake.position = np.array([5,snake.dim-1])
    snake.mv_up()
    assert not snake.alive

def test_mv_down(unSnake):
    snake=unSnake
    snake.dir='b'
    snake.mv_down()
    assert snake.position[1] == 5
    
    snake.position =np.array([5,0])
    snake.mv_down()
    print(snake.position)
    assert not snake.alive

    snake.alive=True
    snake.position = np.array([5,snake.dim-1])
    snake.mv_down()
    assert snake.alive

def test_mv_left(unSnake):
    snake=unSnake
    snake.mv_left()
    assert snake.position[0] == 1
    
    snake.position =np.array([0,4])
    snake.mv_left()
    assert not snake.alive

    snake.alive=True
    snake.position = np.array([snake.dim-1,4])
    snake.mv_left()
    assert snake.alive

def test_mv_right(unSnake):
    snake=unSnake
    snake.mv_right()
    assert snake.position[0] == 3
    
    snake.position =np.array([0,4])
    snake.mv_right()
    assert snake.alive

    snake.alive=True
    snake.position = np.array([snake.dim-1,4])
    snake.mv_right()
    assert not snake.alive

def test_mv_right(unSnake):
    snake=unSnake
    snake.mv_right()
    assert snake.position[0] == 3
    
    snake.position =np.array([0,4])
    snake.mv_right()
    assert snake.alive

    snake.alive=True
    snake.position = np.array([snake.dim-1,4])
    snake.mv_right()
    assert not snake.alive

def test_rel_mv(unSnake):
    snake=unSnake
    snake.rel_mv_front()
    assert snake.position[0] == 2
    assert snake.position[1] == 7

    snake.rel_mv_left()
    assert snake.position[0] == 1
    assert snake.position[1] == 7
    
    snake.rel_mv_left()
    assert snake.position[0] == 1
    assert snake.position[1] == 6

    snake.rel_mv_left()
    assert snake.position[0] == 2
    assert snake.position[1] == 6

def test_bonus(unSnake):
    s=unSnake
    s.bonus=np.array([2,7])
    s.mv_up()
    s.mv_up()
    assert np.array_equal(np.array([2,7]),s.tail[0])
    s.bonus=np.array([5,8])
    s.mv_right()
    s.mv_right()
    assert len(s.tail) ==1
    s.mv_right()
    assert len(s.tail) ==1
    s.mv_right()
    assert len(s.tail) ==2
    s.mv_right()
    assert len(s.tail) ==2

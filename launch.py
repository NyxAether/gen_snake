
from snake import Snake

s=Snake(3)
# s.display()
while s.alive:
    s.display()
    key=input()
    switcher={
        'z':s.mv_up,
        's':s.mv_down,
        'q':s.mv_left,
        'd':s.mv_right,
    }
    switcher[key]()
    
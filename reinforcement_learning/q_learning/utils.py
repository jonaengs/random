from collections import namedtuple

Coordinate = namedtuple("Coordinate", ("x", "y"))
# Used to an action like "up" into a change in coordinates like (x += 0, y += 1)
ActionContainer = namedtuple("ActionContainer", ("up", "right", "down", "left"))
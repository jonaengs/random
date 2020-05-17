import turtle
import random
from bin_tree_draw import place_turtle

# from here: https://en.wikipedia.org/wiki/L-system

vs = ('X', 'F')
cs = ('+', '-', '[', ']')
axiom = 'X'
rules = {'X': ' F+[[X]-X]-F[-FX]+X', 'F': 'FF'}  # backup: {'X': ' F+[[X]-X]-F[-FX]+X', 'F': 'FF'}

def evolve(s, n=1):
    for i in range(n):
        new = ""
        for c in s:
            new += rules.get(c, c)
        s = new
    return s

line_len = 5
draw_speed = 50
degs = lambda: random.randint(20, 30)
def draw(s):
    screen = turtle.getscreen()
    screen.tracer(draw_speed)
    t = turtle.Turtle()
    t.hideturtle()
    place_turtle(t, (-270, -350), 70)
    
    stack = []
    for c in s:
        {'F': lambda: t.fd(line_len),
        '-': lambda: t.rt(degs()),
        '+': lambda: t.lt(degs()),
        '[': lambda: stack.append((t.pos(), t.heading())),
        ']': lambda: place_turtle(t, *stack.pop())
        }.get(c, lambda:None)()
    
    turtle.done()


draw(evolve(axiom, n=6))
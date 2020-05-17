import turtle


# from here: https://en.wikipedia.org/wiki/L-system

vs = ('0', '1')
cs = ('[', ']')
axiom = '0'
rules = {'1': '11', '0': '1[0]0'}


def evolve(s, n=1):
    if n == 0:
        return s

    new = ""
    for c in s:
        new += rules.get(c, c)
    return evolve(new, n-1)


def place_turtle(turtle, pos, angle):
    turtle.penup()
    turtle.goto(pos)
    turtle.setheading(angle)
    turtle.pendown()

line_len = 10
start_pos = (0, -300)
def draw(s):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(8)
    place_turtle(t, start_pos, 90)

    stack = []  # [(pos, angle), ]
    for c in s:
        if c in vs:
            t.fd(line_len)
        elif c == '[':
            stack.append((t.pos(), t.heading()))
            t.lt(45)
        elif c == ']':
            pos, angle = stack.pop()
            place_turtle(t, pos, angle)
            t.rt(45)

    turtle.done()


if __name__ == '__main__':
    draw(evolve(axiom, n=5))
from dataclasses import dataclass, fields
from operator import attrgetter

import pygame
from time import sleep

@dataclass
class Element:
    shape: str
    width: int
    height: int
    function: str = None
    rotation: int = 0
    x: int = 0
    y: int = 0

    @staticmethod
    def field_names():
        return list(map(attrgetter("name"), fields(Element)))

    def as_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Course:
    required_elems = ["spawn", "hole"]

    def __init__(self):
        self.elements = []

    def validate(self):
        assert type(self.width) == type(self.height) == int
        assert self.width > 0 and self.height > 0
        assert all(any(e.function == attr for e in self.elements) for attr in Course.required_elems)

    def show(self):
        def draw_triangle(screen, color, rect):
            points = [(rect.x, rect.y), (rect.x + rect.width, rect.y), (rect.x + rect.width/2, rect.y + rect.height)]
            shape = pygame.draw.polygon(screen, color, points)
            return shape
            
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        screen.fill(pygame.Color("white"))

        draw_funcs = {"rectangle": pygame.draw.rect, "ellipse": pygame.draw.ellipse, "triangle": draw_triangle}
        for e in self.elements:
            draw_funcs.get(e.shape, lambda *x: print("invalid shape: ", e.shape))(
                screen, pygame.Color("black"), e.as_rect()
            )
        
        pygame.display.flip()
        sleep(5)  

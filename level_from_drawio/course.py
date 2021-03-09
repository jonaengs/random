from tkinter import Tk, Canvas, Frame, BOTH
from dataclasses import dataclass, fields


@dataclass
class Element:
    style: str
    width: int
    height: int
    x: int = 0
    y: int = 0

    def get_shape(self):
        return self.x, self.y, self.width, self.height

    def get_shifted(self, course_width, course_height):
        return course_width - self.x, course_height - self.y, self.width, self.height


class Course:
    required = ["spawn", "hole", "width", "height"]

    @staticmethod
    def get_shape_method(canvas, style):
        return {
            "rectangle": canvas.create_rectangle,
            "elipse": canvas.create_oval
        }.get(style, lambda *x, **y: x)

    
    def __init__(self):
        self.elements = []

    def validate(self):
        assert all(hasattr(self, attr) for attr in Course.required)

    def show(self):
        # https://zetcode.com/tkinter/drawing/
        frame = Frame()
        frame.pack(fill=BOTH, expand=1)
        canvas = Canvas(frame, width=self.width, height=self.height)
        for elem in self.elements:
            self.get_shape_method(canvas, elem.style)(*elem.get_shifted(self.width, self.height), fill="red")

        canvas.pack(fill=BOTH, expand=1)
        tk = Tk()
        tk.mainloop()
            




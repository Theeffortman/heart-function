import random
from math import sin, cos, pi, log
from tkinter import *

# def uniform_function (a,b):
#     c = (a+b)/2
#     return c
# def check_number(user_input,random_number):
#     if user_input < random_number:
#         print("random_number is lager than user_input")
#     else :
#         print("random number is smaller than user_input")
#     if random_number > uniform_function(1,20) :
#         print("random number is lager than uniform_function")
#     else:
#         print("random number is less than or equal to uniform_function")
# random_number = random.randint(1,20)
# user_input = int(input("input a number during 1 to 20:"))
# while user_input != random_number:
#     check_number(user_input,random_number)
#     user_input = int(input("input another number during 1 to 20:"))
# print("that's great",user_input)
# Example question: an employee need to have a name and a salary;
# a manager is an employee that leads a team;
# a developer is an employee who knows a programming language

# /////////////////////////////////////////////////////////////////

# class Employee:
#     def __init__(self,name,salary):
#         self.name = name
#         self.salary = salary
#     def set_name (self):
#         self.name = input("type your name:")
#     def set_salary (self):
#         self.salary = input ("type your salary in the company in one year:")
#
# class Manager(Employee):
#     def __init__(self,name):
#         super().__init__(self, name)
#     def set_leader (self):
#         print("a manager is an employee that leads a team")
#         return
#     def set_developer (self):
#         print("a developer is an employee who knows a programming language")
#
#
# if __name__ == "__main__":
#     e = Employee("",0)
#     m = Manager(Employee)
#     e.set_name()
#     e.set_salary()
#     m.set_leader()
#     m.set_developer()
#     print (e.name,e.salary,m.set_leader,m.set_developer)
# //////////////////////////////////////////////////
CANVAS_WIDTH = 840
CANVAS_HEIGHT = 680
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11

HEART_COLOR = "#0000FF"


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(3 * t))
    x *= IMAGE_ENLARGE
    y *= IMAGE_ENLARGE
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y ** 2)) ** 0.520)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx,y - dy

def curve(p):
    return 2 * (2 * sin(4 * p) / 2 * pi)


class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        point_list = list(self._points)
        for _ in range(10000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.27)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y ** 2)) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 15 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []

        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=-15)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-60, 60)
                y += random.randint(-60, 60)
                size = random.choice((1, 1, 2))
                all_points.append((x, y, size))
                all_points.append((x + 20, y + 20, size))
                all_points.append((x - 20, y - 20, size))
                all_points.append((x + 20, y - 20, size))
                all_points.append((x - 20, y + 20, size))
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete("all")
    render_heart.render(render_canvas, render_frame)
    main.after(1, draw, main, render_heart, render_frame + 1)


if __name__ == "__main__":
    root = Tk()
    canvas = Canvas(root, bg="black", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()


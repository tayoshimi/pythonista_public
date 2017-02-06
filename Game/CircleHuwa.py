from scene import *
import sound
import random
from math import sin, cos, pi
import ui
from colorsys import hsv_to_rgb
A = Action

class Circle (ShapeNode):
    def __init__(self, radius = 20, fill_color = '#ff7777',*args, **kwargs):
        self.radius = radius
        path = ui.Path.oval(0, 0, radius, radius)
        ShapeNode.__init__(self, path, fill_color, 'clear', None, *args, **kwargs)
        self.size = Size(self.radius * 2, self.radius * 2)

    def set_rand_move_to(self):
        d = random.uniform(3.0, 8.0)
        dpos = Point(random.uniform(20, self.parent.size.w-20), random.uniform(20, self.parent.size.h-20))
        actions = [A.move_to(dpos.x, dpos.y, d, TIMING_EASE_OUT), A.call(self.set_rand_move_to)]
        self.run_action(A.sequence(actions))

    # Set move by
    def set_rand_move_by(self):
        t = random.uniform(1.0, 6.0)
        d = random.uniform(20.0, 80.0)
        dx, dy = 0, 0

        while True:
            angle = random.uniform(0, pi*2)
            dx = d * cos(angle)
            dy = d * sin(angle)

            if self.is_backframe_intersect(dx, dy):
                break


        actions = [A.move_by(dx, dy, t, TIMING_LINEAR), A.call(self.set_rand_move_by)]
        self.run_action(A.sequence(actions))

    def is_backframe_intersect(self, dx, dy):
        x, y = self.position.x + dx, self.position.y + dy
        rect = Rect(x - self.radius * 2, y - self.radius * 2, self.bbox.w, self.bbox.h)
        
        return self.parent.bbox.intersects(rect)

class MyScene (Scene):
    def setup(self):
        self.items = []
        self.background_color = '#000000'
        self.create_rand_objs(60)


    def create_obj(self, x, y):
        r = random.uniform(30, 60)
        orb = Circle(radius = r, parent = self)
        #orb.position = Point(10,10)
        orb.position = (x, y)
        hue = random.random()
        r, g, b = hsv_to_rgb(hue, 1, 1)
        orb.fill_color = (r,g,b, 0.7)
        orb.set_rand_move_by()
        self.items.append(orb)

    def create_rand_objs(self, num = 20):
        for i in range(num):
            r = random.uniform(30, 60)
            orb = Circle(radius = r, parent = self)
            #orb.position = Point(10,10)
            orb.position = (random.uniform(r, self.size.w-r), random.uniform(r, self.size.h-r))
            hue = random.random()
            r, g, b = hsv_to_rgb(hue, 1, 1)
            orb.fill_color = (r,g,b, 0.7)
            orb.set_rand_move_by()
            self.items.append(orb)


    def did_change_size(self):
        pass

    def update(self):
        for item in self.items:
            if item.paused:
                print('x')

    def touch_began(self, touch):
        self.create_obj(touch.location.x, touch.location.y)
        pass

    def touch_moved(self, touch):
        pass

    def touch_ended(self, touch):
        pass

if __name__ == '__main__':
    run(MyScene(), show_fps=True)


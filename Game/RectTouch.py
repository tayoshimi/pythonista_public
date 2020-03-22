# Square's touch colorlize sample.

from scene import *
#import sound
#import random
#import math
#from colorsys import hsv_to_rgb
from ImageColor import getrgb

A = Action

SQUARE_SIZE = 20
UP_DOWN_SPASE = 40

class Square (ShapeNode):
    id = -1
    def __init__(self, size = SQUARE_SIZE, normal_color = '#fcffb3', touch_color = '#ee1818', select_color = '#ffe999', *args, **kwargs):
        self.size = Size(size, size)
        self.touch_in = False
        self.normal_color = normal_color
        self.touch_color = touch_color
        self.select_color = select_color
        path = ui.Path.rect(0, 0, size, size)
        ShapeNode.__init__(self, path, self.normal_color, 'clear', None, *args, **kwargs)
        
        # Display square's number.
        self.label_node = LabelNode(str(Square.id), font=('<System>', 10), parent = self)
        self.label_node.color = '#caa2ff'
        
        Square.id += 1
    
    def is_touch_in(self, touch):
        x,y,w,h = self.frame.as_tuple()
        touch_x,touch_y = touch.location.as_tuple()
        if x <= touch_x and x + w >= touch_x and y <= touch_y and y + h >= touch_y:
            return True
        else:
            return False

    
    def touch_began(self, touch):
        if self.is_touch_in(touch) and not self.touch_in:
            self.fill_color = self.touch_color
            self.touch_in = True
        
        
    def touch_moved(self, touch):
        if self.is_touch_in(touch) and not self.touch_in:
            self.fill_color = self.touch_color
            self.touch_in = True
        elif not self.is_touch_in(touch) and self.touch_in:
            self.touch_ended(touch)


    def touch_ended(self, touch):
        if self.fill_color != self.normal_color and self.touch_in:
            self.touch_in = False
            self.start_colorlize_action(self.touch_color, self.select_color)
            
    def set_target_color(self):
        self.fill_color = self.target_color
                
    def start_colorlize_action(self, origin_color, target_color):
        self.origin_color = origin_color
        self.target_color = target_color
        self.run_action(A.sequence(A.call(self.colorlize_action, 1.0), A.call(self.set_target_color)))
        
    # Colorize custom action function       
    def colorlize_action(self, node, progress):
        org_r, org_g, org_b = getrgb(self.origin_color)
        t_r, t_g, t_b = getrgb(self.target_color)
        dst_r = (t_r * progress + org_r * (1.0 - progress))
        dst_g = (t_g * progress + org_g * (1.0 - progress))
        dst_b = (t_b * progress + org_b * (1.0 - progress))
        #print(str(dst_r) +','+str(dst_g)+','+str(dst_b))
        self.fill_color = '#%.02X%.02X%.02X' % (int(dst_r), int(dst_g), int(dst_b))


class MyScene (Scene):
    def setup(self):
        self.background_color = '#0d0d0d'
        self.squares = []
               
        i_max = int(self.size.w / SQUARE_SIZE - 0.5) - 2
        j_max = int((self.size.h - UP_DOWN_SPASE * 2 ) / SQUARE_SIZE - 0.5)
        
        # set square's start position
        sx = (self.size.w - SQUARE_SIZE * i_max) / 2
        sy = UP_DOWN_SPASE #(self.size.w - SQUARE_SIZE * i_max) / 2
        
        for i in range(i_max):
            for j in range(j_max):
                square = Square(parent=self)
                x = sx + i * square.size.w
                y = sy + j * square.size.h
                square.position = (x,y)
                self.squares.append(square)

    def did_change_size(self):
        pass

    def update(self):
        pass

    def touch_began(self, touch):
        for square in self.squares:
            square.touch_began(touch)

    def touch_moved(self, touch):
        for square in self.squares:
            square.touch_moved(touch)

    def touch_ended(self, touch):
        for square in self.squares:
            square.touch_ended(touch)

if __name__ == '__main__':
    run(MyScene(), show_fps=True)


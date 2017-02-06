# ColorMixer
# A simple HSV color mixer with three sliders.

import ui
import clipboard
from random import random
from console import hud_alert
import colorsys

def slider_action(sender):
    # Get the root view:
    view = sender.superview
    # Get the sliders:
    h = view['slider1'].value
    s = view['slider2'].value
    v = view['slider3'].value
    # Create the new color from the slider values:
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    view['view1'].background_color = (r, g, b)
    view['label1'].text = '#%.02X%.02X%.02X' % (int(r*255), int(g*255), int(b*255))
    view['label2'].text = 'R,G,B:%.02f,%.02f,%.02f' % (r,g,b)
    view['labelH'].text = 'H:%.02f' % h
    view['labelS'].text = 'S:%.02f' % s
    view['labelV'].text = 'V:%.02f' % v

def copy_action(sender):
    clipboard.set(sender.superview['label1'].text)
    hud_alert('Copied')

def shuffle_action(sender):
    v = sender.superview
    s1 = v['slider1']
    s2 = v['slider2']
    s3 = v['slider3']
    s1.value = random()
    s2.value = random()
    s3.value = random()
    slider_action(s1)

v = ui.load_view('ColorMixerHSV')
slider_action(v['slider1'])
if ui.get_screen_size()[1] >= 768:
    # iPad
    v.present('popover')
else:
    # iPhone
    v.present()


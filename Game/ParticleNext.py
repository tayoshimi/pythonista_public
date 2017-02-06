# Particles
#
# Create colorful bubbles by moving your fingers.

from scene import *
from random import random
from colorsys import hsv_to_rgb

class Particle (object):
	def __init__(self, location, p_size):
		self.velocity = Size(random() * 4 - 2, random() * 4 - 2)
		self.location = Point(location.x,location.y)
		self.p_size = p_size
		self.hue = random()
		self.alpha = 1.0
		
	def draw(self):
		r, g, b = hsv_to_rgb(self.hue, 1, 1)
		a = self.alpha
		tint(r * a, g * a, b * a, a)
		x, y = self.location.as_tuple()
		s = self.p_size
		image('White_Circle', x - s/2, y - s/2, s, s)
		#image('Star_1', x - s/2, y - s/2, s, s)
		self.alpha -= 0.02
		self.hue += 0.02
		self.location.x += self.velocity.w
		self.location.y += self.velocity.h

		

class Particles (Scene):
	def setup(self):
		self.show_instructions = True
		self.particles = set()
		self.p_size = 8 if self.size.w > 700 else 4
	
	def should_rotate(self, orientation):
		return True
	
	def touch_began(self, touch):
		if self.show_instructions:
			self.show_instructions = False
			blend_mode(BLEND_ADD)
	
	def touch_moved(self, touch):
		for t in range(4):
			particle = Particle(touch.location, self.p_size)
			self.particles.add(particle) 
		
	def touch_ended(self, touch):
		for t in range(60):
			particle = Particle(touch.location, self.p_size)
			self.particles.add(particle) 
		
	
	def draw(self):
		background(0, 0, 0)
		if self.show_instructions:
			s = 40 if self.size.w > 700 else 17
			text('Move your fingers across the screen.',
			     'Futura', s, *self.bounds.center().as_tuple())
		dead = set()
		for particle in self.particles:
			particle.draw()
			if particle.alpha <= 0:
				dead.add(particle)
		self.particles -= dead

run(Particles())

# coding: utf-8
# Game of life sample
# 簡易的なGPGPUを実現するために、シェーダーの出力を一旦バッファにセットして、再度シェーダーで計算する

from scene import *
import ui
import io
import numpy as np
from PIL import Image

update_life_shader = '''
precision highp float;
varying vec2 v_tex_coord;
// These uniforms are set automatically:
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec4 u_tint_color;
// This uniform is set in response to touch events:
uniform sampler2D u_state; // 前フレームの情報

int get_state(vec2 offset) {
    return int(texture2D(u_state, (v_tex_coord.xy + offset / u_sprite_size)).r);
}

void main(void) {
  // (-1, 1)に正規化
  vec2 p = v_tex_coord.xy * 2.0 - vec2(1.0, 1.0);
  
  vec4 next_life = vec4(0.0, 0.0, 0.0, 1.0);

  int sum =
        get_state(vec2(-1.0, -1.0)) +
        get_state(vec2(-1.0,  0.0)) +
        get_state(vec2(-1.0,  1.0)) +
        get_state(vec2( 0.0, -1.0)) +
        get_state(vec2( 0.0,  1.0)) +
        get_state(vec2( 1.0, -1.0)) +
        get_state(vec2( 1.0,  0.0)) +
        get_state(vec2( 1.0,  1.0));
    if (sum == 3) {
        next_life = vec4(1.0, 1.0, 1.0, 1.0);
    } else if (sum == 2) {
        float current = float(get_state(vec2(0.0, 0.0)));
        next_life = vec4(current, current, current, 1.0);
    } else {
        //next_life = vec4(0.0, 0.0, 0.0, 1.0);
    }

  gl_FragColor = next_life;
}

'''




render_shader = '''
precision highp float;
varying vec2 v_tex_coord;
// These uniforms are set automatically:
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec4 u_tint_color;
// This uniform is set in response to touch events:
uniform sampler2D u_state;
uniform vec2 u_state_size;
uniform vec2 u_offset;
uniform bool u_f_mouse;

void main(void) {
  vec2 p = v_tex_coord.xy * 2.0 - vec2(1.0, 1.0);
  
  // expand for render sprite. 
  vec4 tex = texture2D(u_state, v_tex_coord / (u_sprite_size / u_state_size));
  
  gl_FragColor = tex * vec4(1., smoothstep(.1, .9, p), 1.);
}
'''

# pil <=> ui
def pil2ui(imgIn):
  with io.BytesIO() as bIO:
    imgIn.save(bIO, 'PNG')
    imgOut = ui.Image.from_data(bIO.getvalue())
  del bIO
  return imgOut


SZ = ui.get_screen_size()

#DRAW_SIZE_W = (SZ.w / 100.0) * 100.0
#DRAW_SIZE_H = (SZ.h / 100.0) * 100.0

DRAW_SIZE_W = SZ.w - 10
DRAW_SIZE_H = SZ.h - 10

# A life point size
EXPANTION_RATE = 2.0

GOL_SIZE_W = DRAW_SIZE_W / EXPANTION_RATE
GOL_SIZE_H = DRAW_SIZE_H / EXPANTION_RATE


class MyScene (Scene):
    def setup(self):   
      self.back_buf = self.make_rand_texture((GOL_SIZE_W, GOL_SIZE_H))
      
      
      self.sprite_life = SpriteNode(parent=self, anchor_point=(0,0))
      self.sprite_life.size = Size(GOL_SIZE_W, GOL_SIZE_H)
      self.sprite_life.shader = Shader(update_life_shader)
      self.sprite_life.shader.set_uniform('u_state', self.back_buf)
      #self.sprite_life.alpha = 0.0
      
           
      # 表示用
      self.sprite_render = SpriteNode(parent=self, size = (DRAW_SIZE_W, DRAW_SIZE_H), anchor_point=(0,0))
      self.sprite_render.shader = Shader(render_shader)
      self.sprite_render.shader.set_uniform('u_state', self.back_buf)
      
      sx, sy = self.sprite_life.size
      self.sprite_render.shader.set_uniform('u_state_size', (sx, sy))
      
      self.did_change_size()
      
      
      
    def make_rand_texture(self, size):
      state = np.random.randint(0, 2, size)
      assert state.shape == size
    
      uiimg = pil2ui(Image.fromarray(np.uint8(state).T * 0xff))
      
      return Texture(uiimg)
      

    def did_change_size(self):
      # Center the image:
      sz = ui.get_screen_size()
      sptz = self.sprite_render.size
      self.sprite_render.position = ((sz.w - sptz.w) / 2, (sz.h - sptz.h) / 2)
      
    def touch_began(self, touch):
      self.set_touch_uniform(touch)

    def touch_moved(self, touch):
      self.set_touch_uniform(touch)
      
    def touch_ended(self, touch):
      #self.sprite.shader.set_uniform('u_f_mouse', False)
      pass


    def set_touch_uniform(self, touch):
      # Center the ripple effect on the touch location by setting the `u_offset` shader uniform:
      dx, dy = self.sprite_life.position - touch.location
      self.sprite_life.shader.set_uniform('u_offset', (dx, dy))
      self.sprite_life.shader.set_uniform('u_f_mouse', True)
      
    def update_backbuf(self):
      #self.sprite_life.alpha = 1.0
      self.back_buf = self.sprite_life.render_to_texture()
      #self.sprite_life.alpha = 0.0
      self.sprite_render.shader.set_uniform('u_state', self.back_buf)
      self.sprite_life.shader.set_uniform('u_state', self.back_buf)
    
    def update(self):
      self.update_backbuf()

def main():
  run(MyScene(), frame_interval=4, show_fps=True)

if __name__ == '__main__':
    main()

# module to control mouse using directions and distances
from typing import Tuple

from talon import Context, Module, canvas, cron, ctrl, cron, screen, ui

import math

class Eagle:
    def __init__(self, width: float, height: float):
        self.enabled = False
        self.canvas = None
        self.job = None
        self.last_pos = None
        self.width = width
        self.height = height
        self.bearing = -1
        self.distance = 0
        self.max_distance = (self.width ** 2 + self.height ** 2) ** 0.5
        
    def enable(self):
        if self.enabled:
            return
        self.enabled = True
        self.last_pos = ctrl.mouse_pos()        
        
        print("position: {}".format(self.last_pos))
        
        screen = ui.main_screen()
        self.width, self.height = screen.width, screen.height
        self.canvas = canvas.Canvas(0, 0, self.width, self.height)

        self.canvas.register('mousemove', self.on_mouse)
        self.canvas.register('draw', self.draw_canvas) 
        # self.canvas.freeze() # uncomment this line for debugging
        print("eagle on...")
        print("Eagle position: {}".format(self.last_pos))
        # uncomment this if the mouse movement event isn't working
        #self.job = cron.interval('1600ms', self.check_mouse)

        print("self.canvas.rect.width: {}".format(self.canvas.rect.width))
        print("self.canvas.rect.height: {}".format(self.canvas.rect.height))

    def disable(self):
        if not self.enabled:
            return
        cron.cancel(self.job)
        self.enabled = False
        self.canvas.close()
        self.canvas = None



    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def draw_canvas(self, canvas):
        paint = canvas.paint
        paint.antialias = True
        paint.color = 'fff'
        paint.font.size = 36
        
        rect = canvas.rect

        cx, cy = self.last_pos

        def pot_of_gold(x,y,distance,bearing):
            return  x + distance * math.sin(math.radians(bearing)), y - distance * math.cos(math.radians(bearing))

        def line_aliased(x,y,distance,bearing, color_main = 'ffffff99', color_alias = '00000099'):
            for off, color in ((0.5, color_alias),(-0.5, color_alias),(0, color_main)):
                paint.color = color
                start_x,start_y = pot_of_gold(x,y,off,bearing + 90)
                finish_x,finish_y = pot_of_gold(start_x,start_y,distance,bearing)
                canvas.draw_line(start_x, start_y, finish_x, finish_y)

        def text_aliased(label,x,y,font_size):
                paint.font.size = font_size
                # outline-white and less transparenth
                paint.color = 'ffffffcc'
                canvas.draw_text(label,x-1,y-1)
                canvas.draw_text(label,x+1,y-1)
                # spine-black and more transparent
                paint.color = '00000077'
                canvas.draw_text(label,x-2,y-2)

        # get spoke parameters
        distance = 5000
        tiny_offset = 10
        small_offset = 225
        small_extent = 50
        large_offset = 200
        large_extent = 100
        label_offset = 320

        # draw diagonals
        for bearing in range(45,359,90):
            start_x,start_y = pot_of_gold(cx,cy,tiny_offset,bearing)
            line_aliased(start_x, start_y, distance, bearing)
        
        # bearing not selected
        if self.bearing  == -1:
            # draw minor spokes
            for bearing in range(0,359,45):
                if bearing % 90 == 0:
                    start_x,start_y = pot_of_gold(cx, cy, large_offset, bearing)
                    line_aliased(start_x, start_y, large_extent, bearing)
            for bearing_x10 in range(0,3590,225):
                bearing = bearing_x10/10
                if bearing % 45 != 0:
                    start_x,start_y = pot_of_gold(cx, cy, small_offset, bearing)
                    line_aliased(start_x, start_y, small_extent, bearing)
            # draw labels for cardinal directions
            paint.color = 'ffffffff'
            for bearing,label in zip([0,90,180,270],['North','East','South','West']):
                start_x,start_y = pot_of_gold(cx,cy,label_offset,bearing)
                text_aliased(label,start_x,start_y,45)
                
        # bearing selected
        else:
            # draw selected bearing line            
            line_aliased(cx, cy, distance, self.bearing, color_main = 'ff9999ff', color_alias = 'ffffff99')
            
            # draw distance hash lines
            for spacing, size in [(100,27),(50,18),(10,12),(500,48)]:
                for i in range(int(self.max_distance/spacing) + 1):
                    for inout in [-1,1]:
                        d = self.distance + spacing * i * inout
                        if d > 0:
                            x,y = pot_of_gold(cx,cy,d,self.bearing)
                            sx,sy = pot_of_gold(x,y,size/2,self.bearing - 90)
                            print("sx,sy: {}".format((sx,sy)))
                            line_aliased(sx,sy,size,self.bearing + 90)
                            # draw labels for big lines
                            if spacing == 500 or (spacing == 100 and i % 5 != 0):
                                if 0 < self.bearing < 180:
                                    # draw text to left
                                    sx,sy = pot_of_gold(sx,sy,5,self.bearing - 90)
                                else:
                                    sx,sy = pot_of_gold(sx,sy,size + 5,self.bearing-90)
                                if spacing == 500:
                                    fs = 27                                
                                else:
                                    fs = 18
                                text_aliased(str(spacing * i),sx,sy,fs)
            
            if self.distance > 0:              
                # UPDATE mouse position
                x,y = pot_of_gold(cx, cy, self.distance, self.bearing)
                print("x moving {} from {} to {}".format(self.distance,cx,x))
                x = max(x,0)
                x = min(x,self.width-1)
                y = max(y,0)
                y = min(y,self.height-1)
                ctrl.mouse_move(x, y)
                self.distance = 0
                self.last_pos = x,y
                            
    def on_mouse(self, event):
        # self.check_mouse()
        pass

    def check_mouse(self):
        pos = ctrl.mouse_pos()
        if pos != self.last_pos:
            x, y = pos
            self.canvas.move(x - self.width // 2, y - self.height // 2)
            self.last_pos = pos

eagle_object = Eagle(5000, 5000)
# eagle_object.enable()

mod = Module()
mod.list('compass_cardinal', desc='compass cardinal directions for relative mouse movement')
mod.tag("eagle_showing", desc="Tag indicates whether the eagle compass is showing")


def parse_cardinal(direction: str, distance: int) -> Tuple[bool, int]:
    x, y = ctrl.mouse_pos()
    if ' ' in direction:
        modifier, direction = direction.split(' ', 1)
        if modifier == 'minor':
            distance *= 5
        if modifier == 'major':
            distance *= 25
    if direction == 'left':
        return True, x - distance
    elif direction == 'right':
        return True, x + distance
    elif direction == 'up':
        return False, y - distance
    elif direction == 'down':
        return False, y + distance
    raise ValueError(f"unsupported cardinal direction: {direction}")

@mod.capture(rule="((north | east | south | west | northeast | southeast | southwest | northwest) [(north | east | south | west | northeast | southeast | southwest | northwest)] | up | down | right | left)")
def bearing_capture(m) -> float:
    """determines bearing from spoken compass direction"""
    print('bearing capture, input: {} | length: {}'.format(m,len(m)))
    def bearing_average(b1,b2):
        difference = ((b2 - b1 + 180) % 360) - 180
        return b1 + difference/2
        
    bearing_lookup = {
        'northeast':45,'southeast':135,'southwest':225,'northwest':315,
        'north':0,'east':90,'south':180,'west':270,
        'up':0,'right':90,'down':180,'left':270
        }
    bearing = None
    for w in range(len(m)-1,-1,-1):
        if bearing == None:
            bearing = bearing_lookup[m[w]]
        else:
            bearing = bearing_average(bearing, bearing_lookup[m[w]])
    print("result: {}".format(bearing))
    return bearing
        
@mod.action_class
class Actions:
    def Eagle_enable():
        """Enable relative mouse guide"""
        eagle_object.enable()
        ctx.tags = ["user.eagle_showing"]
        
    def Eagle_disable():
        """Disable relative mouse guide"""
        eagle_object.disable()
        ctx.tags = []
        
    def Eagle_toggle():
        """Toggle relative mouse guide"""
        eagle_object.toggle()

    def set_cardinal(target: float):
        """set the bearing to a cardinal direction"""
        eagle_object.bearing = target
        print('bearing {}'.format(eagle_object.bearing))

    def move_cardinal(move_degrees: int, target: float):
        """move the bearing direction a certain number of degrees towards a cardinal direction"""
        print('new move cardinal function')
        print("input move_degrees: {}".format(move_degrees))
        print("target: {}".format(target))

        # determine difference between current bearing and target bearing
        delta = (((target - eagle_object.bearing) + 180) % 360) - 180
        
        print("delta: {}".format(delta))

        # limit movement to ensure we don't go past the target direction
        if move_degrees > abs(delta):
            move_degrees = abs(delta)

        print("move_degrees: {}".format(move_degrees))

        # adjust sign of movement if necessary
        if delta < 0:
            move_degrees = -move_degrees
            
        print("move_degrees: {}".format(move_degrees))
            
        # perform movement!
        eagle_object.bearing = (eagle_object.bearing + move_degrees) % 360

        print("result: {}".format(eagle_object.bearing))

    def fly_out(distance: int):
        """move out the specified number of pixels"""
        eagle_object.distance = eagle_object.distance + distance
        
        print("function move_out")
        print("distance: {}".format(eagle_object.distance))

    def fly_back(distance: int):
        """move back toward center the specified number of pixels"""
        eagle_object.bearing = (eagle_object.bearing + 180) % 360
        eagle_object.distance = eagle_object.distance + distance

    def test(d1: float):
        """test function"""
        x = 3

        

ctx = Context()

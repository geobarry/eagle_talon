# module to control mouse using directions and distances
from typing import Tuple
from talon import Context, Module, canvas, cron, ctrl, cron, screen, ui
import math, time
mode_label = {1:'tiny',2:'light',3:'medium',4:'heavy'}
eagle_display_mode = {'heavy':4,'medium':3,'light':2,'tiny':1}

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
        self.mode = 3
        
    def enable(self, bearing = -1):
        self.bearing = bearing
        if self.enabled:
            return
        self.enabled = True
        self.last_pos = ctrl.mouse_pos()        
        screen = ui.main_screen()
        self.width, self.height = screen.width, screen.height
        self.canvas = canvas.Canvas.from_screen(screen)#  canvas.Canvas(0, 0, self.width, self.height)
        self.check_mouse()
        self.canvas.register('mousemove', self.on_mouse)
        self.canvas.register('draw', self.draw_canvas) 
        self.canvas.freeze() # uncomment this line for debugging

        self.job = cron.interval('16ms', self.check_mouse)
        
    def disable(self):
        if not self.enabled:
            return
        cron.cancel(self.job)
        self.enabled = False
        self.canvas.close()
        self.canvas = None

    def pot_of_gold(self,x,y,distance,bearing):
        # calculate next position
        theta = math.radians(bearing)
        x2,y2 = x + distance * math.sin(theta), y - distance * math.cos(theta)
        # make sure it is not off the screen
        # note that the most important equation is :
        # tan(theta) = -dx/dy
        if x2 < 0:
            x2 = 0
            if bearing == 90 or bearing == 270:
                y2 = y
            else:
                y2 = y - (x2 - x) / math.tan(theta)
        if x2 > eagle_object.width - 1:
            x2 = eagle_object.width - 1
            if bearing == 90 or bearing == 270:
                y2 = y
            else:
                y2 = y - (x2 - x) / math.tan(theta)
        if y2 < 0:
            y2 = 0
            x2 = x - (y2 - y) * math.tan(theta)
        if y2 > eagle_object.height - 1:
            y2 = eagle_object.height - 1
            x2 = x - (y2 - y) * math.tan(theta)            
        return x2,y2

    def distance_to_edge(self,x,y,bearing):
        # calculate distance to edge in pixels
        # get math shortcuts
        theta = math.radians(bearing)
        cosine_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        h = eagle_object.height
        w = eagle_object.width
        # get distances in vertical and horizontal directions
        if cosine_theta > 0:
            vertical_distance = y/cosine_theta
        elif cosine_theta < 0:
            vertical_distance = (y-h)/cosine_theta
        else:
            vertical_distance = 9000000
        if sin_theta > 0:
            horizontal_distance = (w-x)/sin_theta
        elif sin_theta < 0:
            horizontal_distance = -x/sin_theta
        else:
            horizontal_distance = 9000000
        # distances minimum of vertical and horizontal distances
        return min(vertical_distance,horizontal_distance)

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

        def line_aliased(x,y,distance,bearing, color_main = 'ffffff99', color_alias = '00000099'):
            for off, color in ((1, color_alias),(-1, color_alias),(0.5, color_main),(-0.5, color_main),(0, color_main)):
                paint.color = color
                start_x,start_y = self.pot_of_gold(x,y,off,bearing + 90)
                finish_x,finish_y = self.pot_of_gold(start_x,start_y,distance,bearing)
                canvas.draw_line(start_x, start_y, finish_x, finish_y)

        def line_thick_aliased(x,y,distance,bearing, color_main = 'ffffff99', color_alias = '00000099'):
            for off, color in ((1.5, color_alias),(-1.5, color_alias),(1, color_main),(-1, color_main),(0.5, color_main),(-0.5, color_main),(0, color_main)):
                paint.color = color
                start_x,start_y = self.pot_of_gold(x,y,off,bearing + 90)
                finish_x,finish_y = self.pot_of_gold(start_x,start_y,distance,bearing)
                canvas.draw_line(start_x, start_y, finish_x, finish_y)

        def text_aliased(label,x,y,font_size):
                paint.font.size = font_size
                # spine-black and more transparent
                paint.color = '00000077'
                canvas.draw_text(label,x-2,y-2)
                canvas.draw_text(label,x+2,y-2)
                canvas.draw_text(label,x+2,y+2)
                canvas.draw_text(label,x-2,y+2)
                canvas.draw_text(label,x-2,y-1)
                canvas.draw_text(label,x+1,y-1)
                canvas.draw_text(label,x+1,y+1)
                canvas.draw_text(label,x-2,y+1)

                # outline-white and less transparent
                paint.color = 'ffffffee'
                canvas.draw_text(label,x,y)
                canvas.draw_text(label,x+1,y-1)

        def left_cardinal(bearing):
            if 45 < bearing <= 135:
                return 'N'
            elif 135 <= bearing <= 225:
                return 'E'
            elif 225 <= bearing <= 315:
                return 'S'
            elif bearing <= 360 and bearing >= 0:
                return 'W'
            else:
                return ''

        def right_cardinal(bearing):
            if 0 <= bearing < 45 or 315 <= bearing <= 360:
                return 'E'
            elif bearing < 135:
                return 'S'
            elif bearing < 225:
                return 'W'
            elif bearing < 315:
                return 'N'
            else:
                return ''

        # get spoke parameters
        distance = 5000
        crosshair_radius = 30
        
        long_crosshair_length = 12
        short_crosshair_length = 5

        inner_compass_radius = 250
        outer_compass_radius = 200
        short_compass_mark_length = 50
        long_compass_mark_length = 100
        label_offset = 25

        max_distance = self.distance_to_edge(cx,cy,self.bearing)

        # DRAW GRID
        startBearing = max(0,self.bearing)
        if mode_label[self.mode] in ['heavy','medium','light','tiny']:
            # draw circular crosshairs around current mouse position
            for bearing_adjust in [0,90,180,270]:
                start_x,start_y = self.pot_of_gold(cx,cy,crosshair_radius-long_crosshair_length,startBearing + bearing_adjust)
                line_aliased(start_x, start_y, long_crosshair_length, startBearing + bearing_adjust, color_main = 'ff9999ff', color_alias = 'ffffff99')
            for bearing_adjust in range(0,360,10):
                if not bearing_adjust % 90 == 0:
                    start_x,start_y = self.pot_of_gold(cx,cy,crosshair_radius - short_crosshair_length,startBearing + bearing_adjust)
                    line_aliased(start_x, start_y, short_crosshair_length, startBearing + bearing_adjust, color_main = 'ff9999ff', color_alias = 'ffffff99')

        if mode_label[self.mode] in ['tiny']: 
            # draw an extra little arrow for tiny display
            start_x,start_y = self.pot_of_gold(cx,cy,crosshair_radius,startBearing)
            line_aliased(start_x, start_y, crosshair_radius * 0.5, startBearing, color_main = 'ff9999ff', color_alias = 'ffffff99')
            start_x,start_y = self.pot_of_gold(cx,cy,crosshair_radius * 1.5, startBearing)
            line_aliased(start_x, start_y, crosshair_radius * 0.25, startBearing + 135, color_main = 'ff9999ff', color_alias = 'ffffff99')
            line_aliased(start_x, start_y, crosshair_radius * 0.25, startBearing - 135, color_main = 'ff9999ff', color_alias = 'ffffff99')
            
        
        # bearing not selected
        if self.bearing  == -1:
            if mode_label[self.mode] in ['heavy','medium','light']:
                # draw cardinal directions and diagonals
                for bearing in range(45,359,90):
                    start_x,start_y = self.pot_of_gold(cx,cy,crosshair_radius,bearing)
                    line_aliased(start_x, start_y, distance, bearing)
                for bearing in range(0,359,45):
                    if bearing % 90 == 0:
                        start_x,start_y = self.pot_of_gold(cx, cy, inner_compass_radius - long_compass_mark_length, bearing)
                        line_aliased(start_x, start_y, long_compass_mark_length, bearing)
            if mode_label[self.mode] in ['heavy','medium']:
                # draw minor spokes
                for bearing_x10 in range(0,3590,225):
                    bearing = bearing_x10/10
                    if bearing % 45 != 0:
                        start_x,start_y = self.pot_of_gold(cx, cy, inner_compass_radius - short_compass_mark_length, bearing)
                        line_aliased(start_x, start_y, short_compass_mark_length, bearing)
            if mode_label[self.mode] in ['heavy','medium','light']:
                # draw labels for cardinal directions
                paint.color = 'ffffffff'
                for bearing,label in zip([0,90,180,270],['North','East','South','West']):
                    start_x,start_y = self.pot_of_gold(cx,cy,inner_compass_radius + label_offset,bearing)
                    text_aliased(label,start_x,start_y,45)
            if mode_label[self.mode] in ['heavy','medium']:
                paint.color = 'DDDDDDDD'
                for bearing,label in zip([45,135,225,315],['NE', 'SE','SW','NW']):
                    start_x,start_y = self.pot_of_gold(cx,cy,inner_compass_radius + label_offset,bearing)
                    text_aliased(label,start_x,start_y,30)
            if mode_label[self.mode] in 'heavy':
                paint.color = 'BBBBBB99'
                for bearing,label in zip([22.5,67.5,112.5,157.5,202.5,247.5,292.5,337.5],['NNE', 'ENE','ESE','SSE','SSW','WSW','WNW','NNW']):
                    start_x,start_y = self.pot_of_gold(cx,cy,inner_compass_radius + label_offset,bearing)
                    text_aliased(label,start_x,start_y,18)
                    
        # bearing selected
        if self.bearing  != -1:            
            # draw distance hash lines
            spacings = []
            label_spacings = []
            if mode_label[self.mode] in ['heavy','medium','light']:
                spacings += [500,100]
                if mode_label[self.mode] in ['heavy','medium']:
                    spacings += [50,10]
                    label_spacings += [100]
            
            spacing_sizes = {500:60,100:39,50:21,10:12}
            if mode_label[self.mode] == 'medium':
                spacing_sizes = {500:60,100:25,50:11,10:3}    
            if mode_label[self.mode] == 'light':
                spacing_sizes = {500:60,100:5,50:3,10:2}    
            for j in range(len(spacings)):
                spacing = spacings[j]
                size = spacing_sizes[spacing]
                for i in range(int(self.max_distance/spacing) + 1):
                    # make sure that we are not hitting a larger spacing
                    if (j == 0) or (((spacing * i) % spacings[j-1]) != 0):
                        for inout in [-1,1]:
                            d = self.distance + spacing * i * inout
                            if d > 0 and d < max_distance:
                                x,y = self.pot_of_gold(cx,cy,d,self.bearing)
                                sx,sy = self.pot_of_gold(x,y,size/2,self.bearing - 90)
                                if spacing == 10:
                                    line_aliased(sx,sy,size,self.bearing + 90)
                                else:
                                    line_thick_aliased(sx,sy,size,self.bearing + 90)
                                # draw crosshairs for display light mode
                                if mode_label[self.mode] == 'light':
                                    sx,sy = self.pot_of_gold(x,y,size/2,self.bearing - 180)
                                    if spacing == 500:
                                        line_aliased(sx,sy,size,self.bearing)

                                # draw labels for big lines
                                if spacing in label_spacings:
                                    if 0 < self.bearing < 180: # draw text to left
                                        sx,sy = self.pot_of_gold(sx,sy,5,self.bearing - 90)
                                    else: # draw text to right
                                        sx,sy = self.pot_of_gold(sx,sy,size + 5,self.bearing-90)
                                    if spacing == 500:
                                        fs = 27                                
                                    else:
                                        fs = 18
                                    text_aliased(str(spacing * i),sx,sy,fs)
            if mode_label[self.mode] in ['heavy']:
                # draw selected bearing line            
                start_x,start_y = self.pot_of_gold(cx,cy,10,self.bearing)
                line_thick_aliased(start_x, start_y, distance, self.bearing, color_main = 'ff9999ff', color_alias = 'ffffff99')
            
            # draw adjacent bearings thirty degrees on either side
            for left_right in [-1,1]:
                if left_right == -1:
                    cardinal = left_cardinal(self.bearing)
                else:
                    cardinal = right_cardinal(self.bearing)
                if mode_label[self.mode] in ['heavy','medium']:
                    # draw full spoke every ten degrees
                    for bearing_adjust in [10,20,30]:
                        b = self.bearing + bearing_adjust * left_right
                        start_distance = min(100,max_distance * 0.5)
                        start_x,start_y = self.pot_of_gold(cx,cy,start_distance,b)
                        if mode_label[self.mode] in ['heavy']:
                            line_aliased(start_x,start_y,distance,b)
                        
                if mode_label[self.mode] in ['heavy','medium']:
                    # determine radii
                    hash_length = spacing_sizes[500]
                    radii = []
                    minimum_interval_ratio = 10
                    if max_distance > minimum_interval_ratio * hash_length:
                        radii = [0.6]
                    if mode_label[self.mode] == 'heavy':
                        if max_distance > 3 * minimum_interval_ratio * hash_length:
                            radii = [0.2,0.5,0.8]
                        elif max_distance > 2 * minimum_interval_ratio * hash_length:
                            radii = [0.35,0.75]
                    # draw dial marks at radii
                    for bearing_adjust in range(31):
                        if bearing_adjust % 10 == 0:
                            hash_length = spacing_sizes[500]/2
                        elif bearing_adjust % 5 == 0:
                            hash_length = spacing_sizes[100]/2    
                        else:
                            hash_length = spacing_sizes[50]/2    
                        b = self.bearing + bearing_adjust * left_right
                        dial_radius = [int(max_distance * x) for x in radii]
                        for out_distance in dial_radius:
                            start_x,start_y = self.pot_of_gold(cx,cy,out_distance - hash_length/2,b)
                            line_aliased(start_x,start_y, hash_length,b)
                            # label spokes every ten degrees
                            if bearing_adjust % 10 == 0:
                                buffer = 10
                                text_x,text_y = self.pot_of_gold(start_x,start_y,buffer+hash_length,b)
                                label = "{}{}".format(str(abs(bearing_adjust)), cardinal)
                                text_aliased(label,text_x,text_y,18)
                                    
    def on_mouse(self, event):
        self.check_mouse()

    def check_mouse(self):
        pos = ctrl.mouse_pos()
        if pos != self.last_pos:
            x, y = pos
            self.last_pos = pos
            self.canvas.move(0,0) # this forces canvas redraw
            

eagle_object = Eagle(5000, 5000)
# eagle_object.enable()

mod = Module()
mod.list('eagle_display_mode', desc = 'amount of information displayed in compass grid')
mod.tag("eagle_showing", desc="Tag indicates whether the eagle compass is showing")

@mod.capture(rule="((north | east | south | west | northeast | southeast | southwest | northwest) [(north | east | south | west | northeast | southeast | southwest | northwest)] | up | down | right | left)")
def bearing_capture(m) -> float:
    """determines bearing from spoken compass direction"""
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
    return bearing

def update_canvas():
    bearing = eagle_object.bearing
    eagle_object.disable()
    eagle_object.enable(bearing)
        
@mod.action_class
class Actions:
    def eagle_enable():
        """Enable relative mouse guide"""
        eagle_object.enable()
        update_canvas()
        ctx.tags = ["user.eagle_showing"]

    def eagle_head_start(bearing: float):
        """enable relative mouse guide and point to given bearing direction"""
        eagle_object.enable(bearing)
        update_canvas()
        ctx.tags = ["user.eagle_showing"]
        
    def eagle_disable():
        """Disable relative mouse guide"""
        eagle_object.disable()
        ctx.tags = []
        
    def eagle_toggle():
        """Toggle relative mouse guide"""
        eagle_object.toggle()

    def set_cardinal(target: float):
        """set the bearing to a cardinal direction"""
        eagle_object.bearing = target
        update_canvas()

    def move_cardinal(move_degrees: int, target: float):
        """move the bearing direction a certain number of degrees towards a cardinal direction"""
        # determine difference between current bearing and target bearing
        delta = (((target - eagle_object.bearing) + 180) % 360) - 180
        
        # limit movement to ensure we don't go past the target direction
        if move_degrees > abs(delta):
            move_degrees = abs(delta)

        # adjust sign of movement if necessary
        if delta < 0:
            move_degrees = -move_degrees
            
        # perform movement!
        eagle_object.bearing = (eagle_object.bearing + move_degrees) % 360
        update_canvas()

    def fly_out(distance: int):
        """move out the specified number of pixels"""
        eagle_object.distance = eagle_object.distance + distance
        cx,cy = eagle_object.last_pos        
        x,y = eagle_object.pot_of_gold(cx, cy, distance, eagle_object.bearing)
        ctrl.mouse_move(x, y)
        eagle_object.distance = 0
        eagle_object.last_pos = x,y
        update_canvas()

    def reverse():
        """reverse direction"""
        eagle_object.bearing = (eagle_object.bearing + 180) % 360        
        update_canvas()

    def fly_back(distance: int):
        """turn around and move back the specified number of pixels"""
        cx,cy = eagle_object.last_pos        
        reverse_bearing = (eagle_object.bearing + 180) % 360
        x,y = eagle_object.pot_of_gold(cx, cy, distance, reverse_bearing)
        ctrl.mouse_move(x, y)
        eagle_object.distance = 0
        eagle_object.last_pos = x,y
        update_canvas()
        
    def center_eagle():
        """move mouse to center of screen"""
        x,y = int(eagle_object.width/2), int(eagle_object.height/2)
        ctrl.mouse_move(x,y)
        eagle_object.last_pos = x,y
        update_canvas()

    def display_mode(mode: str):
        """change how much information is displayed in the compass grid"""
        eagle_object.mode = eagle_display_mode[mode]
        update_canvas()

    def test(d1: float):
        """test function"""
        x = 3

ctx = Context()
ctx.lists['user.eagle_display_mode'] = ['heavy','medium','light','tiny']# eagle_display_mode.keys()
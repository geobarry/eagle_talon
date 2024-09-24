mode: user.compass
-
# COMMANDS THAT WILL EXIT COMPASS, INCLUDING MOUSE COMMANDS
exit compass: 
	user.eagle_disable()
	
(touch | click):
	mouse_click(0)
	user.eagle_disable()
(righty | right click):
	mouse_click(1)
	user.eagle_disable()
drag end:
    user.mouse_drag_end(0)
	user.eagle_disable()
(double click | dub click | duke):
	mouse_click() 
	mouse_click()
	user.eagle_disable()

wheel down: 
	user.mouse_scroll_down()
	user.eagle_disable()
wheel tiny [down]: 
	user.mouse_scroll_down(0.2)
	user.eagle_disable()
wheel downer: 
	user.mouse_scroll_down_continuous()
	user.eagle_disable()
wheel up: 
	user.mouse_scroll_up()
	user.eagle_disable()
wheel tiny up: 
	user.mouse_scroll_up(0.2)
	user.eagle_disable()
wheel upper: 
	user.mouse_scroll_up_continuous()
	user.eagle_disable()
wheel left: 
	user.mouse_scroll_left()
	user.eagle_disable()
wheel tiny left: 
	user.mouse_scroll_left(0.5)
	user.eagle_disable()
wheel right: 
	user.mouse_scroll_right()
	user.eagle_disable()
wheel tiny right: 
	user.mouse_scroll_right(0.5)
	user.eagle_disable()


# MOUSE COMMANDS THAT WILL NOT EXIT COMPASS
drag: user.mouse_drag(0)

# SET DIRECTION
# set the movement direction to a compasss direction, e.g. 'north-northeast','up'
[compass] <user.bearing>$:	user.eagle_set_bearing(user.bearing)
# reverse direction  
[compass] reverse$: user.reverse()

# ROTATE
# rotate compass bearing towards a compass direction, e.g. '30 (east|right)'
[compass] <number> [degrees] <user.bearing>$: user.move_cardinal(number, user.bearing)
nudge <user.bearing>$: user.move_cardinal(0.3,user.bearing)

# MOVE
# move specified distance in pixels, e.g. '(jump|fly|walk|crawl) five hundred'
(go | out | go out | fly) <number>$: user.fly_out(number,1000)
walk <number>$: user.fly_out(number,3000)
crawl <number>$: user.fly_out(number,8000)

# move backwards specified distance in pixels
backup <number>$: user.fly_back(number)


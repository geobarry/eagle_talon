tag: user.eagle_showing
-
# SHUT DOWN EAGLE
(eagle off|eagle laugh|eagle out|grid off):
	user.eagle_disable()

# CHANGE DISPLAY MODE
eagle display {user.eagle_display_modes}:
	user.display_mode(user.eagle_display_modes)
	
# SET DIRECTION
# set the movement direction to a compasss direction, e.g. 'north-northeast','up'
eagle <user.bearing>:	user.set_cardinal(user.bearing)
# reverse direction  
eagle reverse: user.reverse()

# SET DIRECTION AND MOVE
eagle <user.bearing> jump <number>: 
	user.set_cardinal(user.bearing)
	user.fly_out(number,10)
eagle <user.bearing> fly <number>: 
	user.set_cardinal(user.bearing)
	user.fly_out(number,1000)
eagle <user.bearing> walk <number>: 
	user.set_cardinal(user.bearing)
	user.fly_out(number,3000)
eagle <user.bearing> crawl <number>: 
	user.set_cardinal(user.bearing)
	user.fly_out(number,8000)

# ROTATE
# rotate compass bearing towards a compass direction, e.g. '30 (east|right)'
eagle <number> <user.bearing>: user.move_cardinal(number, user.bearing)
eagle nudge <user.bearing>: user.move_cardinal(0.3!,user.bearing)

# MOVE
# move specified distance in pixels, e.g. '(jump|fly|walk|crawl) five hundred'
eagle jump <number>: user.fly_out(number,10)
eagle fly <number>: user.fly_out(number,1000)
eagle walk <number>: user.fly_out(number,3000)
eagle crawl <number>: user.fly_out(number,8000)

# move backwards specified distance in pixels
eagle (back|backup) <number>: user.fly_back(number)
	
# CATCH COMMON SPEECH MISRECOGNITION ('fly' heard as 'five')
eagle <user.number_string>: user.five_fly_out(number_string)
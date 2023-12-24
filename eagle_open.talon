tag: user.eagle_showing
-
# SHUT DOWN EAGLE
(eagle off|eagle laugh|eagle out|grid off):
	user.eagle_disable()

# a set the bearing direction to a cardinal direction
# for example 'north'
<user.bearing_capture>:
	user.set_cardinal(user.bearing_capture)

# rotate compass bearing the specified degrees towards the specified direction
# for example: '30 east'
<number> <user.bearing_capture>:
	user.move_cardinal(number_1, user.bearing_capture)

# move out specified distance in pixels
# for example 'fly five hundred'
fly <number>:
	user.fly_out(number_1)

# move backwards specified distance in pixels
(back|backup) <number>:
	user.fly_back(number_1)
	
# reverse direction
reverse:
	user.reverse()
	
# change display mode
eagle display {user.eagle_display_modes}:
	user.display_mode(user.eagle_display_modes)
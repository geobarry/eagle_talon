tag: user.eagle_showing
-
# state base direction
# for example: "north"
#{user.compass_cardinal}:
 #   user.set_cardinal(compass_cardinal_1)

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

# test Talon input of optional parameters
test <user.bearing_capture>:
	user.test(user.bearing_capture)

tag: user.eagle_showing
# state base direction
# for example: "north"
#{user.compass_cardinal}:
 #   user.set_cardinal(compass_cardinal_1)

<user.bearing_capture>:
	user.set_cardinal(user.bearing_capture)

# state bearing offset
# for example: "30 east"
<number> <user.bearing_capture>:
	user.move_cardinal(number_1, user.bearing_capture)
fly <number>:
	user.fly_out(number_1)
return <number>:
	user.fly_back(number_1)
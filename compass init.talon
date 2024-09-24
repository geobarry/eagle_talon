compass <user.bearing>$:
	user.eagle_set_bearing(user.bearing)
	mode.enable("user.compass")
	mode.disable("command")
	
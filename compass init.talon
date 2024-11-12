compass <user.bearing>$:
	user.eagle_set_bearing(user.bearing)
	mode.enable("user.compass")
	mode.disable("command")
compass display [mode] {user.compass_display_mode}:
	user.eagle_enable()
	mode.enable("user.compass") 
	user.compass_set_display_mode(compassed_display_mode)
# move the mouse around a little
compass jiggle: user.compass_jiggle()

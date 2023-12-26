tag: user.eagle_showing
-
# SHUT DOWN EAGLE
(eagle off|eagle laugh|eagle out|grid off):
	user.eagle_disable()

# CHANGE DISPLAY MODE
eagle display {user.eagle_display_modes}:
	user.display_mode(user.eagle_display_modes)
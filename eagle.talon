eagle [(on|mouse)]:
    user.eagle_enable()
(eagle off|eagle laugh|eagle out|grid off):
	user.eagle_disable()
eagle <user.bearing_capture>:
	user.eagle_head_start(user.bearing_capture)
eagle center:
	user.center_eagle()
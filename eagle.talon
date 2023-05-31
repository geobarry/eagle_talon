eagle [(on|mouse)]:
    user.Eagle_enable()
(eagle off|eagle out|grid off):
	user.Eagle_disable()
eagle <user.bearing_capture>:
	user.eagle_head_start(user.bearing_capture)
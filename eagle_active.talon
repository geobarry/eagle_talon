os: windows
tag: user.eagle_active
-
# THIS MODULE IS TO CATCH COMMON SPEECH MISRECOGNITIONS
# move out specified distance in pixels
# for example 'fly five hundred'
<user.number_string>:
	user.five_fly_out(number_string)
		
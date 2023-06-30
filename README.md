![Eagle screenshot](https://github.com/geobarry/talon_eagle/assets/13248690/296cf580-3df6-4487-b57d-a51aa4322522)


# Talon Eagle
Talon voice commands to control mouse using a first-person navigation perspective.
# Purpose
This is for people who have already set up talon voice to control their computer, but are looking for a better way to control the mouse using voice commands. Instead of a rectangular grid, Eagle uses a direction-then-distance protocol inspired by conventions used in surveying and navigation. The premise is that it is more natural and intuitive to move your mouse a specified direction and distance than it is to locate items on the screen by their horizontal and vertical positions. Your mileage may vary, but if you are using a standard mouse grid and you find that your brain takes a little while to figure out what number or letter to say, then give Eagle a try!
# Installation
Just copy or clone all files to somewhere in your talon user folder. 
# Usage
A basic sequence of commands goes something like this:  

``` Eagle On ```  
``` North ```  
``` 20 East ```  
``` Fly 300 ```  
``` Touch ```  
``` Eagle Off ```  

Go ahead and give it a whirl...
<br/>
Figure it out? Other than turning Eagle on and off, the basic sequence involves three conceptual steps:
  1. Set an initial bearing direction
  2. Fine-tune the bearing direction 
  3. Move the mouse a given number of pixels
<br/>
This process can be combined with standard Talon mouse control commands in any manner you like. 
<br/>
That's really all you need to get started. Details on individual commands provided below.

# Commands
``` Eagle On ```  
  * starts Eagle  
  * shows a compass rose  

``` <compass direction> ```  
  * set Eagle's bearing to the given compass direction  
  * a navigation grid will appear showing direction adjustments (in degrees) and distances (in pixels)
  * options include ```North``` ```East``` ```South``` ```West``` ```northeast``` ```southeast``` ```southwest``` ```northwest``` ```north-northeast``` ```east-northeast``` ```east-southeast``` ```south-southeast``` ```south-southwest``` ```west-southwest``` ```west-northwest``` ```north-northwest``` ```up``` ```right``` ```down``` ```left```  

``` Eagle <compass direction> ```
  * shortcut to start Eagle and set the initial bearing direction with one command

``` <number> <compass direction> ```  
  * shifts Eagle's bearing by the given number of degrees towards the given compass direction
  * This is actually very flexible - just say a number of degrees followed by any bearing direction in the general vicinity of where you want to go. For example, if your current bearing is northeast and you want to rotate clockwise 5 degrees, you can say "five east", "five south", "five right" or even "five east northeast". At present only integer values are allowed.

``` Fly <number> ```  
  * moves the mouse the specified distance in pixels in the direction of Eagle's current bearing
  * Pro tip: When trying to click on something all the way across the screen, it may be difficult to get the bearing angle to land on exactly where you want to go. In this case, a good strategy is to bring the mouse close to but not quite all the way to your desired destination, then adjust the bearing a little bit and repeat. For example, if you want to hit a target that is 1000 pixels away to the upper right, you could say ```Eagle Northeast``` ```Fly 950``` to get into the general vicinity, then adjust the bearing more precisely for the final 50 pixels.   

``` (Reverse|Back|Backup) <number> ```
  * moves the mouse backwards the specified distance in pixels

``` Eagle Off ```  
  * closes Eagle and hides the navigation grid or compass rose
# Feedback
This is a work in progress. Any feedback on how to improve it would be welcome!

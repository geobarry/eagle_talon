# Talon Eagle
Talon voice commands to control mouse using a first-person navigation perspective.
# Purpose
This is for people who have already set up talon voice to control their computer, but are looking for a better way to control the mouse using voice commands. Instead of a rectangular grid, Eagle uses a direction-then-distance protocol inspired by conventions used in surveying and navigation. 
# Installation
Clone it to your talon user folder, just like any other set of talon control files. 
# Basic Usage Example
A basic sequence of commands goes something like this:  
``` Eagle On ```  
``` North ```  
``` 20 East ```  
``` Fly 300 ```  
``` Touch ```  
``` Eagle Off ```  
# Detailed Commands
``` Eagle On ```  
  * starts Eagle  
  * shows a compass rose  

``` <compass direction> ```  
  * set Eagle's bearing to the given compass direction  
  * a navigation grid will appear showing direction adjustments (in degrees) and distances (in pixels)
  * options include ```North``` ```East``` ```South``` ```West```  

``` <number> <compass direction> ```  
  * shifts Eagle's bearing the given number of degrees towards the given compass direction  
  
``` Fly 300 ```  .............. move the mouse a specified distance in pixels
``` Touch ```  ................ use standard talon mouse commands at any time
``` Eagle Off ```  ............ hide the navigation grid or compass rose

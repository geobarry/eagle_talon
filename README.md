# Talon Eagle
Talon voice commands to control mouse using a first-person navigation perspective.
# Purpose
This is for people who have already set up talon voice to control their computer, but are looking for a better way to control the mouse using voice commands. Instead of a rectangular grid, Eagle uses a direction-then-distance protocol inspired by conventions used in surveying and navigation. 
# Installation
Clone it to your talon user folder, just like any other set of talon control files. 
# Usage Example
A basic sequence of commands goes something like this:  

``` Eagle On ```  
``` North ```  
``` 20 East ```  
``` Fly 300 ```  
``` Touch ```  
``` Eagle Off ```  
# Commands
``` Eagle On ```  
  * starts Eagle  
  * shows a compass rose  

``` <compass direction> ```  
  * set Eagle's bearing to the given compass direction  
  * a navigation grid will appear showing direction adjustments (in degrees) and distances (in pixels)
  * options include ```North``` ```East``` ```South``` ```West``` ```northeast``` ```southeast``` ```southwest``` ```northwest``` ```north-northeast``` ```east-northeast``` ```east-southeast``` ```south-southeast``` ```south-southwest``` ```west-southwest``` ```west-northwest``` ```north-northwest``` ```up``` ```right``` ```down``` ```left```  

``` <number> <compass direction> ```  
  * shifts Eagle's bearing by the given number of degrees towards the given compass direction  

``` Fly <number> ```  
  * moves the mouse the specified distance in pixels in the direction of Eagle's current bearing  

``` Eagle Off ```  
  * closes Eagle and hides the navigation grid or compass rose

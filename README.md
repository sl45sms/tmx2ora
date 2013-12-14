tmx2ora
=======

Create a layered OpenRaster image from TMX Map Format (tiled)


Why? 
For a game i need a large number of pre rendered images..  
Tiled help's a lot to create the visuals for the game but i need to add final touch on them.  
    
Why OpenRaster?  
As of version 2.8 Gimp can open this image file format.. Also is the native format of mypaint (not tested yet)  
  
Requirements:  
 
PythonMagick, ElementTree 
 
On Ubuntu 13.10  
sudo apt-get install python-lxml python-pythonmagick 
 
Limitations 
Only one tileset, Alpha code... stay tuned... 

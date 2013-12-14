tmx2ora
=======

Create a layered [OpenRaster](http://www.freedesktop.org/wiki/Specifications/OpenRaster/ "OpenRaster") image from [TMX Map Format](https://github.com/bjorn/tiled/wiki/TMX-Map-Format "TMX Map Format") ([Tiled](https://github.com/bjorn/tiled "Tiled"))


Why? 
For a game i need a large number of pre rendered images..  
Tiled help's a lot to create the visuals for the game but i need to add final touch on them.  
    
Why OpenRaster?  
As of version 2.8 [Gimp](http://www.gimp.org/ "Gimp") can open this image file format.. Also is the native format of [MyPaint](http://mypaint.intilinux.com/ "MyPaint") (not tested yet)  
  
Requirements:  
PythonMagick, ElementTree 
 
On Ubuntu 13.10  
sudo apt-get install python-lxml python-pythonmagick 
 
Limitations:  
Only one tileset, 
Layer data as CSV
Alpha code... stay tuned... 

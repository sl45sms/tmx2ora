#!/usr/bin/env python

#
# Copyright (C) 2013 by Panagiotis Skarvelis <sl45sms@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import tempfile, zipfile, os
try:
 import xml.etree.cElementTree as ET
except ImportError:
 import xml.etree.ElementTree as ET
import PythonMagick as Magick

#Get CSV as char array
def getLayerData(layer):
 for data in layer:
  if data.attrib['encoding']!='csv': 
	 print "Sory Only CSV encoding supported"
	 exit(1)
  return data.text.replace('\n', '').split(',')


########################################################################
#TODO command line parammeters
TMX = ET.parse("athina.xml")  #change here as needed
map = TMX.getroot()

#set globals
orientation=map.attrib['orientation'] 
width=int(map.attrib['width'])
height=int(map.attrib['height'])
tilewidth=int(map.attrib['tilewidth'])
tileheight=int(map.attrib['tileheight'])
tilesetimage = map.find('tileset/image')
tilesetimgsrc=tilesetimage.attrib['source'] #TODO For the moment only one(the first) tileset supported
tilesetimgwidth=int(tilesetimage.attrib['width'])
tilesetimgheight=int(tilesetimage.attrib['height'])
#load tilesetimage
tilesetimageraw=file(tilesetimgsrc,'rb').read()

outimagewidth=int(width)*int(tilewidth)
outimageheight=int(height)*int(tileheight)

#prepare xml
tmpfolder = tempfile.mkdtemp('_tmx2ora')
datafolder = tmpfolder+'/data'
thumbnailfolder = tmpfolder+'/Thumbnails'
os.mkdir(datafolder)
os.mkdir(thumbnailfolder)

#build image attributes
image = ET.Element('image')
stack = ET.SubElement(image, 'stack')
oraxml = image.attrib
oraxml['w'] = str(outimagewidth)
oraxml['h'] = str(outimageheight)

imgcount=0
#parse layers 
for path in map:
    tagtype=path.tag
    if tagtype == 'layer':
     print 'layer'
     #create canvas image
     canvas = Magick.Image(Magick.Geometry(outimagewidth,outimageheight),"transparent")
     canvas.magick('PNG')
     gidarray = getLayerData(path)
     for y in range(0, height):
         for x in range(0,width):
             Gid = x+(width * y)
             Tid =  int(gidarray[Gid])
             if Tid != 0:
                TidX = (Tid*tilewidth % tilesetimgwidth)-tilewidth #giati thelei -32?
                TidY = ((Tid/(tilesetimgwidth/tilewidth))*tileheight % tilesetimgheight)
                PosX = x * tilewidth
                PosY = y * tileheight            
                tsi = Magick.Image(Magick.Blob(tilesetimageraw)) 
                tsi.crop(Magick.Geometry(tilewidth,tileheight,TidX,TidY)) #or string "WxH+x+y" 
                canvas.composite(tsi,PosX,PosY,Magick.CompositeOperator.CopyCompositeOp)
     imgcount+=1
     canvas.write(datafolder+'/'+str(imgcount)+"_"+path.attrib['name']+'.png')
     #create layer 
     layer = ET.Element('layer')
     stack.append(layer)
     layer = layer.attrib
     layer['src'] = 'data/'+path.attrib['name']+'.png'
     layer['name'] = path.attrib['name']
     layer['x'] = '0'
     layer['y'] = '0'
     layer['opacity'] = '1.0'
     layer['visibility'] = 'visible'
     layer['composite-op'] = 'svg:src-over'
    elif tagtype == 'imagelayer':
     print 'image'

#write stack.xml
xml = ET.tostring(image, encoding='UTF-8')
f = open(tmpfolder+'/stack.xml', 'w')
f.write(xml)
f.close()

#create thubnail
#prota ftiaxno ton camva gia authn
canvas = Magick.Image(Magick.Geometry(256,256),"transparent")
canvas.magick('PNG8')
for img in sorted(os.listdir(datafolder)):
    print img
    tsi = Magick.Image(datafolder+"/"+img) 
    tsi.resize("256x256")
    canvas.composite(tsi,0,0,Magick.CompositeOperator.OverCompositeOp)
canvas.write(thumbnailfolder+"/thumbnail.png")

#ok now the zip.....
#write_file_str(orafile, 'mimetype', 'image/openraster') # must be the first file written
ora = zipfile.ZipFile('out.ora', 'w')
ora.writestr('mimetype', 'image/openraster',zipfile.ZIP_STORED)
ora.write(tmpfolder+"/stack.xml","stack.xml",zipfile.ZIP_DEFLATED)
ora.write(thumbnailfolder+"/thumbnail.png","Thumbnails/thumbnail.png",zipfile.ZIP_DEFLATED)

#For every img
for img in os.listdir(datafolder):
    ora.write(datafolder+"/"+img,"data/"+img[2:],zipfile.ZIP_DEFLATED)

ora.close()

#and finaly delete tmpfolder
#TODO

